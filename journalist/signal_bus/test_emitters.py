import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('fge_emitters', HERE / 'emitters.py')
em = importlib.util.module_from_spec(spec)
spec.loader.exec_module(em)

def sample(family):
    return dict(family=family, event_type=em.PROFILES[family][0], event_id='fixture-001',
                source_id='FIXTURE-' + family, source_locator='fixture://local/event',
                source_version='UNKNOWN', object_id='FIXTURE-OBJECT', observation='Synthetic test',
                why_it_matters='Verify emitter adapter', privacy_scope='LOCAL_FIXTURE',
                classification='PROPOSED', evidence_refs=['fixture://local/input'],
                route_to=['JOURNALIST'], occurred_at=None)

class EmitterTests(unittest.TestCase):
    def test_all_ten_families_through_existing_bus_and_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bus = root / 'journalist/signal_bus/bus.py'
            bus.parent.mkdir(parents=True)
            bus.write_bytes((HERE / 'bus.py').read_bytes())
            register = root / 'journalist/dispatches/dispatch_register.jsonl'
            for family in em.PROFILES:
                event = sample(family)
                self.assertEqual(em.emit(event, register)['state'], 'LOCAL_INGRESS_COMMITTED')
                self.assertEqual(em.emit(event, register)['state'], 'LOCAL_INGRESS_REUSED')
            run = lambda cmd: json.loads(subprocess.check_output([sys.executable,str(bus),cmd]))
            self.assertEqual(run('run')['emitted'], 10)
            self.assertEqual(run('validate')['status'], 'PASS')
            self.assertEqual(run('run')['emitted'], 0)
            self.assertEqual((bus.parent / 'acks.jsonl').read_text(), '')

    def test_changed_event_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'events.jsonl'
            event = sample(next(iter(em.PROFILES)))
            em.emit(event, p)
            event['observation'] = 'changed'
            with self.assertRaisesRegex(ValueError, 'IDEMPOTENCY_CONFLICT'):
                em.emit(event, p)
            self.assertEqual(len(p.read_text().splitlines()), 1)

    def test_invalid_input(self):
        base = sample(next(iter(em.PROFILES)))
        for patch in [{'canon_effect':'WRITE'}, {'authority_effect':'GAIN'}, {'family':'OTHER'},
                      {'event_type':'INVENTED'}, {'evidence_refs':[]}, {'route_to':[]},
                      {'classification':'VERIFIED'}, {'source_id':''}, {'occurred_at':'bad'}]:
            with self.subTest(patch=patch), self.assertRaises((ValueError,TypeError)):
                em.prepare(dict(base, **patch))

    def test_unknown_and_extensions_preserved(self):
        event = sample(next(iter(em.PROFILES)))
        event['custom'] = {'unknown':None}
        before = copy.deepcopy(event)
        row = em.prepare(event)
        self.assertEqual(event, before)
        self.assertEqual(row['original_event'], before)
        self.assertEqual(row['provenance']['source_content_sha256'], 'UNKNOWN')
        self.assertIsNone(row['timestamp'])

    def test_corrupt_register_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'events.jsonl'
            p.write_text('broken\n')
            with self.assertRaises(ValueError):
                em.emit(sample(next(iter(em.PROFILES))), p)
            self.assertEqual(p.read_text(), 'broken\n')

if __name__ == '__main__':
    unittest.main()

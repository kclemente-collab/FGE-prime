"""On-demand source-event emitters. No polling, network, or fabricated ACKs."""
import argparse
import fcntl
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

VERSION = '0.1.0'
PROFILES = {
 'GOOGLE_DRIVE/BRAINDOCS': ['DOCUMENT_DISCOVERED','SOURCE_REVISION_OBSERVED','DEPENDENCY_MISSING'],
 'COMPILER_ASSEMBLY_LOG': ['COMPILER_REGISTERED','CONTRACT_CHANGED','CAPABILITY_GAP'],
 'CHARACTER_REGISTRY': ['CHARACTER_REVISION','IDENTITY_COLLISION','ATTRIBUTE_UNKNOWN'],
 'CHARACTER_PORTFOLIO': ['RENDER_CANDIDATE','VISUAL_DRIFT','OUTPUT_VALIDATED'],
 'HB_COMPILER': ['STIMULUS_RESPONSE_DELTA','BEHAVIOR_CANDIDATE'],
 'SCENE_EXPERIENCE_CONSOLE': ['SCENE_STIMULUS','RESPONSE_OBSERVED','CONSEQUENCE_RECORDED'],
 'FASHION/MIRROR/DEVELOP/BUILD': ['CONCEPT_CANDIDATE','DRIFT_FLAG','STORY_VALIDATION','ARTIFACT_VALIDATION'],
 'LINKBASE/TWIN_TOWER_MIRROR': ['CONNECTION_CANDIDATE','DANGLING_EDGE','SOURCE_CONFLICT'],
 'TRIBUNAL/PILOT_SANDBOX': ['TEST_PASSED','TEST_FAILED','READINESS_CANDIDATE'],
 'PRODUCTION/COMMERCIAL': ['PACKAGE_READY_CANDIDATE','RIGHTS_UNKNOWN','RELEASE_BLOCKED'],
}
ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / 'journalist/dispatches/dispatch_register.jsonl'

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)

def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()

def validate(event):
    if not isinstance(event, dict):
        raise ValueError('EVENT_OBJECT_REQUIRED')
    for key in ['family','event_type','event_id','source_id','source_locator','source_version',
                'object_id','observation','why_it_matters','privacy_scope']:
        if not isinstance(event.get(key), str) or not event[key].strip():
            raise ValueError('MISSING_OR_INVALID:' + key)
    if event['family'] not in PROFILES or event['event_type'] not in PROFILES[event['family']]:
        raise ValueError('UNDECLARED_EVENT')
    if event.get('canon_effect', 'NONE') != 'NONE' or event.get('authority_effect', 'NONE') != 'NONE':
        raise ValueError('AUTHORITY_EFFECT_FORBIDDEN')
    if event.get('classification') not in ['OBSERVED','CLAIMED','PROPOSED','UNKNOWN','CONFLICTING']:
        raise ValueError('CLASSIFICATION_REQUIRED')
    for key in ['evidence_refs','route_to']:
        if not isinstance(event.get(key), list) or not event[key] or not all(isinstance(x,str) and x.strip() for x in event[key]):
            raise ValueError('NONEMPTY_LIST_REQUIRED:' + key)
    if 'occurred_at' not in event:
        raise ValueError('OCCURRED_AT_OR_NULL_REQUIRED')
    if event['occurred_at'] is not None:
        dt = datetime.fromisoformat(event['occurred_at'].replace('Z','+00:00'))
        if dt.tzinfo is None:
            raise ValueError('TIMEZONE_REQUIRED')
    canonical(event)

def prepare(event):
    validate(event)
    # Event identity is separate from content: changed bytes with the same identity conflict.
    key = digest([event['family'], event['source_id'], event['event_id']])
    return {
        'dispatch_id': 'FGE-EMIT-' + key,
        'timestamp': event['occurred_at'],
        'recorded_at': datetime.now(timezone.utc).isoformat(),
        'source': event['source_id'], 'status': event['classification'],
        'subject': event['object_id'] + ': ' + event['event_type'],
        'observation': event['observation'], 'route_to': event['route_to'],
        'affects': event['route_to'], 'why_it_matters': event['why_it_matters'],
        'knowledge_delta': 'NEW_EVIDENCE',
        'next_admissible_action': 'Review source evidence; propose only.',
        'canon_effect': 'NONE', 'authority_effect': 'NONE', 'ack_required': True,
        'evidence': event['evidence_refs'],
        'provenance': {'source_locator': event['source_locator'],
                       'source_version': event['source_version'],
                       'source_content_sha256': event.get('source_content_sha256','UNKNOWN'),
                       'event_id': event['event_id'], 'family': event['family'],
                       'privacy_scope': event['privacy_scope'],
                       'emitter_version': VERSION},
        'emitter_input_digest': digest(event),
        'original_event': event,
    }

def emit(event, register=REGISTER):
    row = prepare(event)
    register = Path(register)
    register.parent.mkdir(parents=True, exist_ok=True)
    # Lock covers replay check, append, and fsync. Existing bus reads remain unchanged.
    with register.open('a+', encoding='utf-8') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        stream.seek(0)
        lines = stream.readlines()
        if lines and not lines[-1].endswith('\n'):
            raise ValueError('INCOMPLETE_INGRESS_LINE')
        for line in lines:
            if not line.strip():
                continue
            prior = json.loads(line)  # Corrupt ingress fails closed, never silently skips.
            if prior.get('dispatch_id') == row['dispatch_id']:
                if prior.get('emitter_input_digest') != row['emitter_input_digest']:
                    raise ValueError('IDEMPOTENCY_CONFLICT')
                return {'state':'LOCAL_INGRESS_REUSED','dispatch_id':row['dispatch_id'], 'application_ack':None}
        stream.write(canonical(row) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    return {'state':'LOCAL_INGRESS_COMMITTED','dispatch_id':row['dispatch_id'], 'application_ack':None}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['catalog','prepare','emit'])
    parser.add_argument('--event', type=Path)
    args = parser.parse_args()
    if args.action == 'catalog':
        result = {'version':VERSION, 'profiles':PROFILES, 'mode':'ON_DEMAND',
                  'producer_hooks':'UNBOUND', 'remote_delivery':'UNVERIFIED'}
    else:
        if not args.event:
            parser.error('--event required')
        event = json.loads(args.event.read_text())
        result = prepare(event) if args.action == 'prepare' else emit(event)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()

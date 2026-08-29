import copy
import json
from pathlib import Path
import unittest

from systems.modular_fashion_os.storage.github_store import (
    GitHubAPIError,
    GitHubFashionStore,
    StorageContractError,
    StorageRecoveryRequired,
    StoreConfig,
)


FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "EXAMPLE_NONCANON_fashion_asset.json"


class MemoryStore(GitHubFashionStore):
    def __init__(self):
        super().__init__(StoreConfig(repository="fge/test", token="test"))
        self.files = {}
        self.counter = 0
        self.index_conflicts = 0

    def _read_file(self, path):
        value = self.files.get(path)
        return None if value is None else dict(value)

    def _put_file(self, path, text, message, sha=None):
        if path.endswith("index.json") and self.index_conflicts:
            self.index_conflicts -= 1
            raise GitHubAPIError(409, "simulated concurrent update")
        current = self.files.get(path)
        if current is not None and sha != current["sha"]:
            raise GitHubAPIError(409, "sha mismatch")
        if current is None and sha is not None:
            raise GitHubAPIError(422, "unexpected sha")
        self.counter += 1
        new_sha = f"sha-{self.counter}"
        self.files[path] = {"sha": new_sha, "content": text}
        return {"commit": {"sha": f"commit-{self.counter}"}}


class GitHubFashionStoreTest(unittest.TestCase):
    def setUp(self):
        self.asset = json.loads(FIXTURE.read_text())
        self.store = MemoryStore()

    def test_every_save_validates_full_schema(self):
        invalid = copy.deepcopy(self.asset)
        invalid["rights"]["valuation"]["currency"] = "DOLLARS"
        with self.assertRaises(StorageContractError):
            self.store.save_asset(invalid)

    def test_asset_ids_use_collision_free_path_segments(self):
        slash = copy.deepcopy(self.asset)
        slash["identity"]["asset_id"] = "brand/coat"
        underscore = copy.deepcopy(self.asset)
        underscore["identity"]["asset_id"] = "brand_coat"

        slash_receipt = self.store.save_asset(slash)
        underscore_receipt = self.store.save_asset(underscore)

        self.assertNotEqual(slash_receipt["path"], underscore_receipt["path"])
        self.assertIn("brand%2Fcoat", slash_receipt["path"])
        self.assertEqual(
            self.store.load_asset("brand/coat", slash["version"])["identity"][
                "asset_id"
            ],
            "brand/coat",
        )
        self.assertEqual(
            self.store.load_asset("brand_coat", underscore["version"])["identity"][
                "asset_id"
            ],
            "brand_coat",
        )

    def test_concurrent_index_conflict_recovers(self):
        self.store.index_conflicts = 1
        receipt = self.store.save_asset(self.asset)
        self.assertEqual(receipt["index_state"], "RECOVERED")
        self.assertEqual(receipt["recovery_attempts"], 1)
        loaded = self.store.load_asset(
            self.asset["identity"]["asset_id"], self.asset["version"]
        )
        self.assertEqual(loaded["object_id"], self.asset["object_id"])

    def test_partial_write_can_be_reconciled(self):
        self.store.index_conflicts = 99
        with self.assertRaises(StorageRecoveryRequired):
            self.store.save_asset(self.asset)
        self.store.index_conflicts = 0
        receipt = self.store.reconcile_asset_index(
            self.asset["identity"]["asset_id"], self.asset["version"]
        )
        self.assertEqual(receipt["index_state"], "RECOVERED")

    def test_recovery_revalidates_the_stored_envelope(self):
        path = self.store.asset_path(
            self.asset["identity"]["asset_id"], self.asset["version"]
        )
        invalid = copy.deepcopy(self.asset)
        invalid["rights"]["valuation"]["currency"] = "DOLLARS"
        self.store.files[path] = {
            "sha": "sha-invalid",
            "content": self.store.canonical_json(invalid),
        }
        with self.assertRaises(StorageContractError):
            self.store.reconcile_asset_index(
                self.asset["identity"]["asset_id"], self.asset["version"]
            )

    def test_latest_version_uses_semver_not_write_order(self):
        high = copy.deepcopy(self.asset)
        high["version"] = "0.10.0"
        low = copy.deepcopy(self.asset)
        low["version"] = "0.2.0"
        self.store.save_asset(high)
        self.store.save_asset(low)
        index = self.store.load_index()
        record = index["assets"][self.asset["identity"]["asset_id"]]
        self.assertEqual(record["latest_version"], "0.10.0")


if __name__ == "__main__":
    unittest.main()

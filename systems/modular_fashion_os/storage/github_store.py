"""FGE GitHub-backed persistence for versioned fashion asset envelopes.

Environment variables:
  GITHUB_TOKEN       Fine-grained token with Contents read/write permission.
  GITHUB_REPOSITORY  owner/repository, e.g. kclemente-collab/FGE-prime
  GITHUB_BRANCH      optional, defaults to main

This module stores immutable version records and maintains a small registry index.
It never silently overwrites a version with different content.
"""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

from systems.modular_fashion_os.validation import (
    PACKAGE_ROOT,
    ContractValidationError,
    validate_envelope,
    validate_json_contract,
)


DEFAULT_ROOT = "systems/modular_fashion_os/storage"
MAX_INDEX_RETRIES = 4


class StorageConflict(RuntimeError):
    """Raised when a version already exists with different content."""


class StorageContractError(ValueError):
    """Raised when an envelope lacks the minimum persistence contract."""


class GitHubAPIError(RuntimeError):
    """GitHub API failure retaining its HTTP status for recovery decisions."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        super().__init__(f"GitHub API {status_code}: {detail}")


class StorageRecoveryRequired(RuntimeError):
    """Asset bytes exist but index recovery could not be completed automatically."""

    def __init__(self, asset_id: str, version: str, path: str):
        self.asset_id = asset_id
        self.version = version
        self.path = path
        super().__init__(
            f"Stored {asset_id}@{version} at {path}, but index registration failed; "
            "call reconcile_asset_index()"
        )


@dataclass(frozen=True)
class StoreConfig:
    repository: str
    token: str
    branch: str = "main"
    root: str = DEFAULT_ROOT

    @classmethod
    def from_env(cls) -> "StoreConfig":
        token = os.environ.get("GITHUB_TOKEN", "")
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        if not token:
            raise RuntimeError("GITHUB_TOKEN is required")
        if "/" not in repository:
            raise RuntimeError("GITHUB_REPOSITORY must be owner/repository")
        return cls(
            repository=repository,
            token=token,
            branch=os.environ.get("GITHUB_BRANCH", "main"),
        )


class GitHubFashionStore:
    api_root = "https://api.github.com"

    def __init__(self, config: StoreConfig):
        self.config = config

    def _request(
        self,
        method: str,
        endpoint: str,
        payload: Optional[Dict[str, Any]] = None,
        allow_404: bool = False,
    ) -> Optional[Dict[str, Any]]:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        req = Request(
            f"{self.api_root}{endpoint}",
            data=body,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.config.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
                "User-Agent": "FGE-Modular-Fashion-OS/0.1",
            },
        )
        try:
            with urlopen(req, timeout=30) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except HTTPError as exc:
            if allow_404 and exc.code == 404:
                return None
            detail = exc.read().decode("utf-8", errors="replace")
            raise GitHubAPIError(exc.code, detail) from exc

    def _contents_endpoint(self, path: str) -> str:
        encoded = "/".join(quote(part, safe="") for part in path.split("/"))
        return f"/repos/{self.config.repository}/contents/{encoded}"

    def _read_file(self, path: str) -> Optional[Dict[str, Any]]:
        endpoint = self._contents_endpoint(path)
        result = self._request(
            "GET",
            f"{endpoint}?ref={quote(self.config.branch, safe='')}",
            allow_404=True,
        )
        if result is None:
            return None
        content = base64.b64decode(result["content"]).decode("utf-8")
        return {"sha": result["sha"], "content": content}

    def _put_file(self, path: str, text: str, message: str, sha: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": message,
            "branch": self.config.branch,
            "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
        }
        if sha:
            payload["sha"] = sha
        result = self._request("PUT", self._contents_endpoint(path), payload)
        assert result is not None
        return result

    @staticmethod
    def canonical_json(data: Dict[str, Any]) -> str:
        return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"

    @staticmethod
    def digest(text: str) -> str:
        return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def _validated_receipt(receipt: Dict[str, Any]) -> Dict[str, Any]:
        validate_json_contract(
            receipt,
            PACKAGE_ROOT / "schema" / "payloads" / "storage_module.json",
        )
        return receipt

    @staticmethod
    def _validate_minimum(envelope: Dict[str, Any]) -> tuple[str, str]:
        try:
            validate_envelope(envelope)
        except ContractValidationError as exc:
            raise StorageContractError(str(exc)) from exc
        identity = envelope.get("identity") or {}
        asset_id = identity.get("asset_id")
        version = envelope.get("version")
        if not isinstance(asset_id, str) or not asset_id.strip():
            raise StorageContractError("identity.asset_id is required")
        if not isinstance(version, str) or not version.strip():
            raise StorageContractError("version is required")
        return asset_id, version

    def asset_path(self, asset_id: str, version: str) -> str:
        # Encode each value as one reversible repository path segment. Replacing
        # separators (for example, "/" with "_") is lossy and can make two
        # distinct governed IDs resolve to the same immutable record.
        safe_asset = quote(asset_id, safe="")
        safe_version = quote(version, safe="")
        return f"{self.config.root}/assets/{safe_asset}/{safe_version}.json"

    def load_asset(self, asset_id: str, version: str) -> Optional[Dict[str, Any]]:
        record = self._read_file(self.asset_path(asset_id, version))
        if record is None:
            return None
        envelope = json.loads(record["content"])
        self._validate_minimum(envelope)
        return envelope

    def load_index(self) -> Dict[str, Any]:
        path = f"{self.config.root}/index.json"
        record = self._read_file(path)
        if record is None:
            return {
                "object_id": "FGE-FASHION-STORAGE-INDEX-001",
                "version": "0.2.0",
                "status": "ACTIVE_STORAGE_INDEX",
                "authority": "GITHUB_PERSISTENCE",
                "assets": {},
            }
        return json.loads(record["content"])

    @staticmethod
    def _semver_key(version: str) -> tuple[int, int, int]:
        return tuple(int(part) for part in version.split("."))

    def _index_entry(
        self,
        envelope: Dict[str, Any],
        path: str,
        content_hash: str,
    ) -> Dict[str, Any]:
        return {
            "path": path,
            "content_hash": content_hash,
            "object_id": envelope["object_id"],
            "status": envelope.get("status", "UNKNOWN"),
            "canon_effect": envelope.get("canon_effect", "NONE"),
        }

    def _register_index(
        self,
        envelope: Dict[str, Any],
        path: str,
        content_hash: str,
        *,
        max_attempts: int = MAX_INDEX_RETRIES,
    ) -> Dict[str, Any]:
        """Optimistically update the index, retrying concurrent SHA conflicts."""
        asset_id = envelope["identity"]["asset_id"]
        version = envelope["version"]
        index_path = f"{self.config.root}/index.json"
        last_error: Exception | None = None
        for attempt in range(1, max_attempts + 1):
            index_record = self._read_file(index_path)
            if index_record is None:
                index = {
                    "object_id": "FGE-FASHION-STORAGE-INDEX-001",
                    "version": "0.2.0",
                    "status": "ACTIVE_STORAGE_INDEX",
                    "authority": "GITHUB_PERSISTENCE",
                    "assets": {},
                }
            else:
                index = json.loads(index_record["content"])
            assets = index.setdefault("assets", {})
            asset_record = assets.setdefault(asset_id, {"versions": {}})
            versions = asset_record.setdefault("versions", {})
            versions[version] = self._index_entry(envelope, path, content_hash)
            asset_record["latest_version"] = max(versions, key=self._semver_key)
            try:
                result = self._put_file(
                    index_path,
                    self.canonical_json(index),
                    f"Register fashion asset {asset_id}@{version}",
                    sha=None if index_record is None else index_record["sha"],
                )
                return {
                    "result": result,
                    "attempts": attempt,
                    "recovered": attempt > 1,
                }
            except GitHubAPIError as exc:
                last_error = exc
                if exc.status_code not in (409, 422):
                    raise
        assert last_error is not None
        raise last_error

    def reconcile_asset_index(self, asset_id: str, version: str) -> Dict[str, Any]:
        """Recover an orphaned immutable asset into the registry index."""
        path = self.asset_path(asset_id, version)
        stored = self._read_file(path)
        if stored is None:
            raise FileNotFoundError(path)
        envelope = json.loads(stored["content"])
        stored_asset_id, stored_version = self._validate_minimum(envelope)
        if (stored_asset_id, stored_version) != (asset_id, version):
            raise StorageConflict("Stored path and envelope identity disagree")
        content_hash = self.digest(self.canonical_json(envelope))
        registration = self._register_index(envelope, path, content_hash)
        return self._validated_receipt({
            "receipt_type": "FGE_FASHION_STORAGE_RECEIPT",
            "asset_id": asset_id,
            "version": version,
            "path": path,
            "content_hash": content_hash,
            "asset_commit": None,
            "index_commit": registration["result"].get("commit", {}).get("sha"),
            "authority": "GITHUB_PERSISTENCE",
            "index_state": "RECOVERED",
            "recovery_attempts": registration["attempts"],
        })

    def save_asset(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        """Persist one immutable asset version and register it.

        If the version exists with identical canonical content, the operation is idempotent.
        If it exists with different content, StorageConflict is raised.
        """
        # Detach the caller-owned object before validation so the exact snapshot
        # that passes the contract is the snapshot written and indexed.
        payload = copy.deepcopy(envelope)
        asset_id, version = self._validate_minimum(payload)
        text = self.canonical_json(payload)
        content_hash = self.digest(text)
        path = self.asset_path(asset_id, version)

        existing = self._read_file(path)
        if existing is not None:
            existing_hash = self.digest(existing["content"])
            if existing_hash != content_hash:
                raise StorageConflict(
                    f"{asset_id}@{version} already exists with different content; create a new version"
                )
            asset_commit = None
        else:
            try:
                result = self._put_file(
                    path,
                    text,
                    f"Store fashion asset {asset_id}@{version}",
                )
                asset_commit = result.get("commit", {}).get("sha")
            except GitHubAPIError as exc:
                if exc.status_code not in (409, 422):
                    raise
                raced = self._read_file(path)
                if raced is None or self.digest(raced["content"]) != content_hash:
                    raise StorageConflict(
                        f"Concurrent writer stored different content for {asset_id}@{version}"
                    ) from exc
                asset_commit = None

        try:
            registration = self._register_index(payload, path, content_hash)
        except Exception as exc:
            raise StorageRecoveryRequired(asset_id, version, path) from exc
        index_result = registration["result"]

        return self._validated_receipt({
            "receipt_type": "FGE_FASHION_STORAGE_RECEIPT",
            "asset_id": asset_id,
            "version": version,
            "path": path,
            "content_hash": content_hash,
            "asset_commit": asset_commit,
            "index_commit": index_result.get("commit", {}).get("sha"),
            "authority": "GITHUB_PERSISTENCE",
            "index_state": "RECOVERED" if registration["recovered"] else "REGISTERED",
            "recovery_attempts": registration["attempts"] - 1,
        })


if __name__ == "__main__":
    raise SystemExit(
        "Import GitHubFashionStore from this module; do not execute it without an explicit envelope."
    )

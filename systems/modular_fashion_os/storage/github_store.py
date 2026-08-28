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


DEFAULT_ROOT = "systems/modular_fashion_os/storage"


class StorageConflict(RuntimeError):
    """Raised when a version already exists with different content."""


class StorageContractError(ValueError):
    """Raised when an envelope lacks the minimum persistence contract."""


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
            raise RuntimeError(f"GitHub API {exc.code}: {detail}") from exc

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
    def _validate_minimum(envelope: Dict[str, Any]) -> tuple[str, str]:
        for field in ("object_id", "version", "identity", "provenance", "garment", "representations", "validation"):
            if field not in envelope:
                raise StorageContractError(f"Missing required field: {field}")
        identity = envelope.get("identity") or {}
        asset_id = identity.get("asset_id")
        version = envelope.get("version")
        if not isinstance(asset_id, str) or not asset_id.strip():
            raise StorageContractError("identity.asset_id is required")
        if not isinstance(version, str) or not version.strip():
            raise StorageContractError("version is required")
        return asset_id, version

    def asset_path(self, asset_id: str, version: str) -> str:
        safe_asset = asset_id.replace("/", "_")
        safe_version = version.replace("/", "_")
        return f"{self.config.root}/assets/{safe_asset}/{safe_version}.json"

    def load_asset(self, asset_id: str, version: str) -> Optional[Dict[str, Any]]:
        record = self._read_file(self.asset_path(asset_id, version))
        return None if record is None else json.loads(record["content"])

    def load_index(self) -> Dict[str, Any]:
        path = f"{self.config.root}/index.json"
        record = self._read_file(path)
        if record is None:
            return {
                "object_id": "FGE-FASHION-STORAGE-INDEX-001",
                "version": "0.1.0",
                "status": "ACTIVE_STORAGE_INDEX",
                "authority": "GITHUB_PERSISTENCE",
                "assets": {},
            }
        return json.loads(record["content"])

    def save_asset(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        """Persist one immutable asset version and register it.

        If the version exists with identical canonical content, the operation is idempotent.
        If it exists with different content, StorageConflict is raised.
        """
        asset_id, version = self._validate_minimum(envelope)
        payload = copy.deepcopy(envelope)
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
            result = self._put_file(
                path,
                text,
                f"Store fashion asset {asset_id}@{version}",
            )
            asset_commit = result.get("commit", {}).get("sha")

        index_path = f"{self.config.root}/index.json"
        index_record = self._read_file(index_path)
        index = self.load_index()
        assets = index.setdefault("assets", {})
        record = assets.setdefault(asset_id, {"versions": {}})
        record["versions"][version] = {
            "path": path,
            "content_hash": content_hash,
            "object_id": envelope["object_id"],
            "status": envelope.get("status", "UNKNOWN"),
            "canon_effect": envelope.get("canon_effect", "NONE"),
        }
        record["latest_version"] = version

        index_result = self._put_file(
            index_path,
            self.canonical_json(index),
            f"Register fashion asset {asset_id}@{version}",
            sha=None if index_record is None else index_record["sha"],
        )

        return {
            "receipt_type": "FGE_FASHION_STORAGE_RECEIPT",
            "asset_id": asset_id,
            "version": version,
            "path": path,
            "content_hash": content_hash,
            "asset_commit": asset_commit,
            "index_commit": index_result.get("commit", {}).get("sha"),
            "authority": "GITHUB_PERSISTENCE",
        }


if __name__ == "__main__":
    raise SystemExit(
        "Import GitHubFashionStore from this module; do not execute it without an explicit envelope."
    )

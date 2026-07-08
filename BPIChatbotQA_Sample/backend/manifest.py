import hashlib
import json
import os
import time
from pathlib import Path


def file_sha256(path: str) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def load_manifest(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_manifest(manifest: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = f"{path}.tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    os.replace(temp_path, path)


def _rel_path(base_path: str, file_path: str) -> str:
    return str(Path(file_path).resolve().relative_to(Path(base_path).resolve())).replace("\\", "/")


def scan_documents(docs_path: str, supported_exts: set[str], excluded: list[str]) -> dict:
    path = Path(docs_path)
    excluded_lower = {f.lower() for f in excluded}
    scanned = {}
    if not path.exists():
        return scanned

    for file_path in path.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in supported_exts:
            continue
        if file_path.name.startswith("~$") or file_path.name.startswith(".") or file_path.name.endswith(".tmp"):
            continue
        if file_path.name.lower() in excluded_lower:
            continue
        try:
            rel_path = _rel_path(docs_path, str(file_path))
            stat = file_path.stat()
            scanned[rel_path] = {
                "relative_path": rel_path,
                "source_file": file_path.name,
                "absolute_path": str(file_path),
                "sha256": file_sha256(str(file_path)),
                "mtime": stat.st_mtime,
                "size": stat.st_size,
            }
        except Exception:
            continue
    return scanned


def changed_files(manifest: dict, docs_path: str, supported_exts: set[str], excluded: list[str]):
    scanned = scan_documents(docs_path, supported_exts, excluded)
    manifest_keys = set(manifest.keys())
    scanned_keys = set(scanned.keys())

    added = [scanned[k] for k in sorted(scanned_keys - manifest_keys)]
    deleted = [manifest[k] for k in sorted(manifest_keys - scanned_keys)]
    modified = []
    unchanged = []

    for key in sorted(manifest_keys & scanned_keys):
        current = scanned[key]
        previous = manifest[key]
        if previous.get("sha256") != current.get("sha256"):
            modified.append(current)
        else:
            unchanged.append(current)

    return {
        "scanned": scanned,
        "added": added,
        "modified": modified,
        "deleted": deleted,
        "unchanged": unchanged,
        "scanned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

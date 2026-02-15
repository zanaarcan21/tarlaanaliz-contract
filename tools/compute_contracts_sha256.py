#!/usr/bin/env python3
"""
Compute deterministic SHA-256 over the contracts repo "material" files.
Used for pinning in CONTRACTS_VERSION.md and for consumer verification.

Material set (default):
- schemas/**.json
- enums/**.json
- api/**.yaml|yml
- ssot/**.md
- docs/** (optional, included by default because examples/migration guides affect validation)

Rules:
- Paths are normalized to POSIX.
- Hash is over concatenation of: <path>\n<sha256(file_bytes)>\n for each file sorted lexicographically.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path

DEFAULT_GLOBS = [
    "schemas/**/*.json",
    "enums/**/*.json",
    "api/**/*.yaml",
    "api/**/*.yml",
    "ssot/**/*.md",
    "docs/**/*",
]

def file_sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="repo root")
    ap.add_argument("--no-docs", action="store_true", help="exclude docs/** from material set")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    globs = list(DEFAULT_GLOBS)
    if args.no_docs:
        globs = [g for g in globs if not g.startswith("docs/")]

    files: list[Path] = []
    for g in globs:
        for p in root.glob(g):
            if p.is_file():
                files.append(p)

    # Deterministic order by relative POSIX path
    rels = sorted({p.relative_to(root).as_posix(): p for p in files}.items(), key=lambda kv: kv[0])

    h = hashlib.sha256()
    for rel, p in rels:
        h.update(rel.encode("utf-8"))
        h.update(b"\n")
        h.update(file_sha256(p).encode("utf-8"))
        h.update(b"\n")

    print(h.hexdigest())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

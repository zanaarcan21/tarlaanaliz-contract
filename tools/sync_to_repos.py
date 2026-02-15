#!/usr/bin/env python3
"""
Sync this contracts repo into consumer repos as vendor snapshot:

Consumer layout (recommended):
- <consumer_repo>/vendor/contracts/  (readonly snapshot)
- <consumer_repo>/CONTRACTS_VERSION.md  (must match semver+sha256)

This script:
1) Clones or updates consumer repos
2) Copies material files into vendor/contracts
3) Copies CONTRACTS_VERSION.md to repo root
4) Commits and opens PR (optionally) using GitHub CLI (gh) if available.

Authentication:
- For PR creation, expects GH_TOKEN env and `gh` installed in CI.
"""
from __future__ import annotations
import argparse
import os
import shutil
import subprocess
from pathlib import Path

MATERIAL_DIRS = ["schemas", "enums", "api", "ssot", "docs"]
MATERIAL_FILES = ["CONTRACTS_VERSION.md", "CHANGELOG.md", "README.md", "LICENSE", "package.json", "pyproject.toml"]

def run(cmd: list[str], cwd: Path | None = None) -> str:
    return subprocess.check_output(cmd, cwd=str(cwd) if cwd else None, text=True).strip()

def ensure_repo(url: str, dest: Path) -> None:
    if dest.exists():
        run(["git", "fetch", "--all"], cwd=dest)
        run(["git", "checkout", "main"], cwd=dest)
        run(["git", "pull", "--ff-only"], cwd=dest)
    else:
        run(["git", "clone", url, str(dest)])

def copy_snapshot(src_root: Path, dst_repo: Path, vendor_path: str) -> None:
    dst_vendor = dst_repo / vendor_path
    if dst_vendor.exists():
        shutil.rmtree(dst_vendor)
    dst_vendor.mkdir(parents=True, exist_ok=True)

    # Copy dirs
    for d in MATERIAL_DIRS:
        s = src_root / d
        if s.exists():
            shutil.copytree(s, dst_vendor / d, dirs_exist_ok=True)

    # Copy key files into vendor root
    for f in MATERIAL_FILES:
        s = src_root / f
        if s.exists():
            shutil.copy2(s, dst_vendor / f)

    # Copy CONTRACTS_VERSION.md to repo root
    shutil.copy2(src_root / "CONTRACTS_VERSION.md", dst_repo / "CONTRACTS_VERSION.md")

def create_branch_and_pr(dst_repo: Path, branch: str, title: str, body: str) -> None:
    run(["git", "checkout", "-b", branch], cwd=dst_repo)
    run(["git", "add", "-A"], cwd=dst_repo)
    # Allow no-op
    status = run(["git", "status", "--porcelain"], cwd=dst_repo)
    if not status:
        print(f"No changes in {dst_repo.name}; skipping PR.")
        run(["git", "checkout", "main"], cwd=dst_repo)
        run(["git", "branch", "-D", branch], cwd=dst_repo)
        return

    run(["git", "commit", "-m", title], cwd=dst_repo)
    run(["git", "push", "--set-upstream", "origin", branch], cwd=dst_repo)

    # Create PR via gh if available
    try:
        run(["gh", "pr", "create", "--title", title, "--body", body, "--head", branch], cwd=dst_repo)
    except Exception as e:
        print(f"PR create skipped/failed (ensure gh+auth): {e}")

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contracts-root", default=".", help="contracts repo root")
    ap.add_argument("--workdir", default=".sync_work", help="temp workdir")
    ap.add_argument("--vendor-path", default="vendor/contracts", help="destination snapshot folder in consumer repos")
    ap.add_argument("--consumer", action="append", required=True,
                    help="consumer spec: <name>=<git_url> e.g. platform=https://github.com/org/repo")
    ap.add_argument("--create-pr", action="store_true")
    ap.add_argument("--branch-prefix", default="chore/contracts-sync")
    args = ap.parse_args()

    src_root = Path(args.contracts_root).resolve()
    workdir = Path(args.workdir).resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    semver = run(["python", "tools/read_contracts_version.py"], cwd=src_root) if (src_root/"tools/read_contracts_version.py").exists() else "unknown"

    for spec in args.consumer:
        name, url = spec.split("=", 1)
        dst_repo = workdir / name
        ensure_repo(url, dst_repo)
        copy_snapshot(src_root, dst_repo, args.vendor_path)

        if args.create_pr:
            branch = f"{args.branch_prefix}/{semver}"
            title = f"chore(contracts): sync {semver}"
            body = f"Automated contracts snapshot sync from contracts repo. Version: {semver}"
            create_branch_and_pr(dst_repo, branch, title, body)
        else:
            print(f"Prepared snapshot for {name} at {dst_repo}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())

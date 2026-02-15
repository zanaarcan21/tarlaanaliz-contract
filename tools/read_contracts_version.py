#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path

def main() -> int:
    p = Path("CONTRACTS_VERSION.md")
    t = p.read_text(encoding="utf-8")
    m = re.search(r"^semver:\s*(v\d+\.\d+\.\d+)\s*$", t, re.MULTILINE)
    if not m:
        raise SystemExit("semver not found")
    print(m.group(1))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

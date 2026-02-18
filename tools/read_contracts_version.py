#!/usr/bin/env python3
"""BOUND:TOOLS_READ_CONTRACTS_VERSION"""
from __future__ import annotations
import re
from pathlib import Path

def main() -> int:
    p = Path("CONTRACTS_VERSION.md")
    t = p.read_text(encoding="utf-8")
    m = re.search(r"^version:\s*(\d+\.\d+\.\d+)\s*$", t, re.MULTILINE)
    if not m:
        raise SystemExit("version not found")
    print(m.group(1))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

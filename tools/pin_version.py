#!/usr/bin/env python3
"""
TarlaAnaliz Contracts Version Pinner

Manages contract versioning with semantic versioning and SHA-256 checksums.
Updates CONTRACTS_VERSION.md with new version and file hashes.

Usage:
    python3 tools/pin_version.py --version 1.2.0 --breaking
    python3 tools/pin_version.py --patch  # Auto-increment patch
    python3 tools/pin_version.py --minor  # Auto-increment minor
    python3 tools/pin_version.py --major  # Auto-increment major (breaking)
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


class VersionPinner:
    """Manages contract version pinning with SHA-256 checksums"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.contracts_file = base_dir / "CONTRACTS_VERSION.md"
        self.schemas_dir = base_dir / "schemas"
        self.api_dir = base_dir / "api"
        
    def compute_file_hash(self, file_path: Path) -> str:
        """Compute SHA-256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def compute_directory_hash(self, directory: Path, pattern: str = "*.json") -> str:
        """Compute combined SHA-256 hash of all matching files in directory"""
        files = sorted(directory.rglob(pattern))
        combined_hash = hashlib.sha256()
        
        for file_path in files:
            file_hash = self.compute_file_hash(file_path)
            # Combine relative path and hash for deterministic ordering
            combined_hash.update(f"{file_path.relative_to(directory)}:{file_hash}".encode())
        
        return combined_hash.hexdigest()
    
    def get_current_version(self) -> Tuple[int, int, int]:
        """Parse current version from CONTRACTS_VERSION.md"""
        if not self.contracts_file.exists():
            return (0, 0, 0)
        
        with open(self.contracts_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'## Version: (\d+)\.(\d+)\.(\d+)', content)
        if match:
            return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return (0, 0, 0)
    
    def increment_version(self, version_type: str) -> Tuple[int, int, int]:
        """Increment version based on type"""
        major, minor, patch = self.get_current_version()
        
        if version_type == 'major':
            return (major + 1, 0, 0)
        elif version_type == 'minor':
            return (major, minor + 1, 0)
        elif version_type == 'patch':
            return (major, minor, patch + 1)
        else:
            raise ValueError(f"Invalid version type: {version_type}")
    
    def collect_file_hashes(self) -> Dict[str, str]:
        """Collect SHA-256 hashes of all contract files"""
        hashes = {}
        
        # Schema files
        for schema_file in self.schemas_dir.rglob('*.json'):
            rel_path = schema_file.relative_to(self.base_dir)
            hashes[str(rel_path)] = self.compute_file_hash(schema_file)
        
        # API files
        for api_file in self.api_dir.rglob('*.yaml'):
            rel_path = api_file.relative_to(self.base_dir)
            hashes[str(rel_path)] = self.compute_file_hash(api_file)
        
        return hashes
    
    def compute_contracts_checksum(self, file_hashes: Dict[str, str]) -> str:
        """Compute overall contracts checksum from individual file hashes"""
        combined_hash = hashlib.sha256()
        
        # Sort by path for deterministic ordering
        for file_path in sorted(file_hashes.keys()):
            combined_hash.update(f"{file_path}:{file_hashes[file_path]}".encode())
        
        return combined_hash.hexdigest()
    
    def generate_version_file(
        self, 
        version: Tuple[int, int, int],
        is_breaking: bool,
        changelog_entry: str = None
    ) -> str:
        """Generate CONTRACTS_VERSION.md content"""
        major, minor, patch = version
        version_str = f"{major}.{minor}.{patch}"
        
        file_hashes = self.collect_file_hashes()
        contracts_checksum = self.compute_contracts_checksum(file_hashes)
        
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        content = f"""# TarlaAnaliz Contracts Version Lock

## Version: {version_str}

**Release Date:** {timestamp}  
**Breaking Change:** {'YES' if is_breaking else 'NO'}  
**Contracts Checksum (SHA-256):** `{contracts_checksum}`

---

## Version Policy

This file locks the contract version for all consumers (platform, edge, worker).
Consumers MUST validate the contracts checksum before use.

**Semantic Versioning:**
- **MAJOR** (breaking): Incompatible schema changes (field removal, type change, enum removal)
- **MINOR** (non-breaking): New optional fields, new enums, new schemas
- **PATCH** (fixes): Documentation updates, examples, metadata

**Breaking Change Rules:**
- Field removal or rename → MAJOR
- Required field addition → MAJOR
- Type change → MAJOR
- Enum value removal → MAJOR
- Schema removal → MAJOR

**Non-Breaking Changes:**
- Optional field addition → MINOR
- New enum value → MINOR
- New schema → MINOR
- Description/example update → PATCH

---

## File Checksums (SHA-256)

Individual file hashes for verification:

"""
        
        # Group files by category
        categories = {
            'Shared Schemas': [],
            'Enums': [],
            'Core Schemas': [],
            'Edge Schemas': [],
            'Worker Schemas': [],
            'Events': [],
            'Platform': [],
            'API Components': [],
            'API Specs': []
        }
        
        for file_path, file_hash in sorted(file_hashes.items()):
            if 'schemas/shared' in file_path:
                categories['Shared Schemas'].append((file_path, file_hash))
            elif 'schemas/enums' in file_path:
                categories['Enums'].append((file_path, file_hash))
            elif 'schemas/core' in file_path:
                categories['Core Schemas'].append((file_path, file_hash))
            elif 'schemas/edge' in file_path:
                categories['Edge Schemas'].append((file_path, file_hash))
            elif 'schemas/worker' in file_path:
                categories['Worker Schemas'].append((file_path, file_hash))
            elif 'schemas/events' in file_path:
                categories['Events'].append((file_path, file_hash))
            elif 'schemas/platform' in file_path:
                categories['Platform'].append((file_path, file_hash))
            elif 'api/components' in file_path:
                categories['API Components'].append((file_path, file_hash))
            elif 'api/' in file_path:
                categories['API Specs'].append((file_path, file_hash))
        
        # Output by category
        for category, files in categories.items():
            if files:
                content += f"### {category}\n\n"
                for file_path, file_hash in files:
                    content += f"- `{file_path}`  \n  `{file_hash}`\n"
                content += "\n"
        
        # Changelog section
        content += """---

## Changelog

"""
        
        if changelog_entry:
            content += f"### v{version_str} ({timestamp[:10]})\n\n"
            content += f"**Breaking:** {'YES' if is_breaking else 'NO'}\n\n"
            content += f"{changelog_entry}\n\n"
        else:
            content += f"### v{version_str} ({timestamp[:10]})\n\n"
            content += f"**Breaking:** {'YES' if is_breaking else 'NO'}\n\n"
            content += "Version pinned automatically.\n\n"
        
        # Verification instructions
        content += """---

## Verification

Consumers MUST verify contracts checksum:

### Python
```python
import hashlib
import json

def verify_contracts(expected_checksum: str) -> bool:
    # Compute actual checksum from schemas
    actual_checksum = compute_contracts_checksum()
    return actual_checksum == expected_checksum

assert verify_contracts("{checksum}"), "Contracts checksum mismatch!"
```

### Node.js
```javascript
const crypto = require('crypto');
const assert = require('assert');

function verifyContracts(expectedChecksum) {{
  const actualChecksum = computeContractsChecksum();
  return actualChecksum === expectedChecksum;
}}

assert(verifyContracts("{checksum}"), "Contracts checksum mismatch!");
```

### CI/CD Integration

Add to `.github/workflows/validate.yml`:

```yaml
- name: Verify Contracts Version
  run: |
    python3 tools/pin_version.py --verify
```

---

## Consumer Integration

### Platform Service (platform repo)
```bash
# In platform repo
git submodule add https://github.com/tarlaanaliz/contracts contracts
git submodule update --remote
python3 contracts/tools/pin_version.py --verify
```

### Edge Station (edge repo)
```bash
# In edge repo
git submodule add https://github.com/tarlaanaliz/contracts contracts
git submodule update --remote
./contracts/tools/sync_to_repos.sh --target edge
```

### Worker Service (worker repo)
```bash
# In worker repo
git submodule add https://github.com/tarlaanaliz/contracts contracts
git submodule update --remote
./contracts/tools/sync_to_repos.sh --target worker
```

---

## Notes

- **Immutable:** Once released, versions are immutable. Create new version for changes.
- **CI Enforcement:** All PRs MUST pass `tools/validate.py` and checksum verification.
- **Breaking Changes:** Require major version bump and consumer coordination.
- **Hash Algorithm:** SHA-256 (collision-resistant, FIPS 140-2 compliant)
- **Timestamp:** ISO 8601 UTC format

**Last Updated:** {timestamp}
""".format(checksum=contracts_checksum, timestamp=timestamp)
        
        return content
    
    def verify_checksums(self) -> bool:
        """Verify current checksums match pinned version"""
        if not self.contracts_file.exists():
            print("❌ CONTRACTS_VERSION.md not found")
            return False
        
        with open(self.contracts_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract expected checksum
        match = re.search(r'Contracts Checksum \(SHA-256\):\*\* `([a-f0-9]{64})`', content)
        if not match:
            print("❌ Could not parse checksum from CONTRACTS_VERSION.md")
            return False
        
        expected_checksum = match.group(1)
        
        # Compute actual checksum
        file_hashes = self.collect_file_hashes()
        actual_checksum = self.compute_contracts_checksum(file_hashes)
        
        if actual_checksum == expected_checksum:
            print(f"✅ Checksums match: {actual_checksum}")
            return True
        else:
            print(f"❌ Checksum mismatch!")
            print(f"   Expected: {expected_checksum}")
            print(f"   Actual:   {actual_checksum}")
            return False
    
    def pin_version(
        self,
        version: Tuple[int, int, int] = None,
        version_type: str = None,
        is_breaking: bool = False,
        changelog: str = None
    ) -> bool:
        """Pin new version"""
        
        # Determine version
        if version:
            major, minor, patch = version
        elif version_type:
            major, minor, patch = self.increment_version(version_type)
            # MAJOR bump enforced for breaking changes
            if is_breaking and version_type != 'major':
                print("⚠️  WARNING: Breaking change detected but not major bump")
                print("    Forcing MAJOR version bump")
                current = self.get_current_version()
                major, minor, patch = (current[0] + 1, 0, 0)
        else:
            # Default: patch increment
            major, minor, patch = self.increment_version('patch')
        
        version_str = f"{major}.{minor}.{patch}"
        
        print(f"📌 Pinning version {version_str}")
        print(f"   Breaking: {is_breaking}")
        
        # Generate version file
        content = self.generate_version_file(
            version=(major, minor, patch),
            is_breaking=is_breaking,
            changelog_entry=changelog
        )
        
        # Write to file
        with open(self.contracts_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Version {version_str} pinned successfully")
        print(f"   File: {self.contracts_file}")
        
        return True


def main():
    """Main CLI"""
    parser = argparse.ArgumentParser(
        description='Pin TarlaAnaliz contract version with checksums',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--version', help='Explicit version (e.g., 1.2.0)')
    group.add_argument('--major', action='store_true', help='Increment major version (breaking)')
    group.add_argument('--minor', action='store_true', help='Increment minor version')
    group.add_argument('--patch', action='store_true', help='Increment patch version')
    group.add_argument('--verify', action='store_true', help='Verify checksums only')
    
    parser.add_argument('--breaking', action='store_true', help='Mark as breaking change')
    parser.add_argument('--changelog', help='Changelog entry')
    
    args = parser.parse_args()
    
    # Find base directory
    base_dir = Path(__file__).parent.parent
    pinner = VersionPinner(base_dir)
    
    # Verify mode
    if args.verify:
        print("🔍 Verifying contracts checksums...\n")
        if pinner.verify_checksums():
            print("\n✅ Verification successful")
            sys.exit(0)
        else:
            print("\n❌ Verification failed")
            sys.exit(1)
    
    # Pin version
    if args.version:
        # Parse explicit version
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', args.version)
        if not match:
            print(f"❌ Invalid version format: {args.version}")
            print("   Expected: MAJOR.MINOR.PATCH (e.g., 1.2.0)")
            sys.exit(1)
        version = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        pinner.pin_version(version=version, is_breaking=args.breaking, changelog=args.changelog)
    elif args.major:
        pinner.pin_version(version_type='major', is_breaking=True, changelog=args.changelog)
    elif args.minor:
        pinner.pin_version(version_type='minor', is_breaking=args.breaking, changelog=args.changelog)
    elif args.patch:
        pinner.pin_version(version_type='patch', is_breaking=False, changelog=args.changelog)
    else:
        # Default: patch increment
        pinner.pin_version(version_type='patch', changelog=args.changelog)
    
    # Verify after pinning
    print("\n🔍 Verifying pinned version...")
    if pinner.verify_checksums():
        print("✅ Version pinned and verified")
        sys.exit(0)
    else:
        print("❌ Verification failed after pinning")
        sys.exit(1)


if __name__ == '__main__':
    main()
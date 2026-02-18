# TarlaAnaliz Contracts Version Lock

## Version: 0.0.1

**Release Date:** 2026-02-18T16:44:58.765180Z  
**Breaking Change:** NO  
**Contracts Checksum (SHA-256):** `c737c45d0b5b8647b7745587da398a723afba0c4bc98054fc5541c04957e2cc7`

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

### Shared Schemas

- `schemas/shared/address.v1.schema.json`  
  `9edecd639a7a4440f66c887aedeab9f255208d0f9e50723f08905023cf398665`
- `schemas/shared/geojson.v1.schema.json`  
  `af385a0c07b80dfdc0f4565d6e743d40d32612a59625e7b756ecb9e2b1c952a8`
- `schemas/shared/money.v1.schema.json`  
  `64fc425b2c734fd51c79bf43fa4a3f85572b4c48fcbead8215e506202250ec2e`

### Core Schemas

- `schemas/core/field.v1.schema.json`  
  `4d3663595905f69437436ab9a478deeb2eab23ac6ebf420525a827c454afc0d1`
- `schemas/core/mission.v1.schema.json`  
  `8343b08777db73a50340843d48d15466176463f2c29b4b86cd71ec5236bcc02f`
- `schemas/core/user.v1.schema.json`  
  `0802c8ef44ffd24ee7ad7900acc28f19e9d9de8e24d58d6d1d5860ba5d6c6634`
- `schemas/core/user_pii.v1.schema.json`  
  `8308a63f302188db2ab1ec7be1f34ad0cf14bb74426c2d4a09860d18193af2b6`

### Edge Schemas

- `schemas/edge/edge_metadata.v1.schema.json`  
  `d081229b4092d67d1a38e61b994a8d4a83010d695c6b0769c3e31ac80312f851`
- `schemas/edge/intake_manifest.v1.schema.json`  
  `aa44a564750c2e11ba1f81624196a1034f222957180dc5ca3627da096ef790c7`
- `schemas/edge/quarantine_event.v1.schema.json`  
  `8ea1bf0eea7409b4cbfdc5608cda4689970a24eae7bbbfe251b7d66790e6bc94`

### Worker Schemas

- `schemas/worker/analysis_job.v1.schema.json`  
  `426db4ed780e5bb0a7e8bb53fd5ea6564fe02139f96f91102e3e457a92180331`
- `schemas/worker/analysis_result.v1.schema.json`  
  `69af83931b8f8ae66f4f2981362e772a54073f44de6b680c4bf9c32c3ae9f5af`

### Events

- `schemas/events/analysis_completed.v1.schema.json`  
  `6f093470ce2644ffff3bb1e05c9148a2650723e7f4420dcddd81f228006a4db6`
- `schemas/events/field_created.v1.schema.json`  
  `9fb0649f1d2e214553f4afc4148cf3ebf6358e9f9dcb0effd83188f0370e1035`
- `schemas/events/mission_assigned.v1.schema.json`  
  `6a3d4a6cb0b286cfa4f35fa8cab41a8d5fe04c410c90f8bb83a59cdeee77f2c3`

### Platform

- `schemas/platform/calibrated_dataset_manifest.v1.schema.json`  
  `4cad336bb3edfb05be2345707c5e98a02c6386d3ca480f7dac677a32f81dca17`
- `schemas/platform/calibration_result.v1.schema.json`  
  `244d859ee9f3658d2206dd3c5df2483fed98909f4b727634a4190ad06c1332a9`
- `schemas/platform/layer_registry.v1.schema.json`  
  `5d011bbb71c6cb236a163205b8ad9b159db3f66ae5ce8002b6f8d71412635eb9`
- `schemas/platform/payment_intent.v1.schema.json`  
  `6ef25f66008a64915fac13723383b5f4a6e432b5f86a0354930ac425733406bd`
- `schemas/platform/payment_intent.v2.schema.json`  
  `63e3cbc267598d47f3eb33ea50fa90f455b0dba7a23ba200d2ff06d58d94b8e1`
- `schemas/platform/payroll.v1.schema.json`  
  `72817e6ee06fd533dbeede4127cd024f71ad59c2572a5de2c42d78066590bc1c`
- `schemas/platform/pricing.v1.schema.json`  
  `b6270875d14eeedd116024443cd4681de803974ef1495e41f970a1ba782ef778`
- `schemas/platform/qc_report.v1.schema.json`  
  `0709dd9c98ebaa11c45924bf571b0cfb6291af16711fbb133e1e2e7b3d97a538`

### API Components

- `api/components/parameters.yaml`  
  `19cc0b99a8ec6873037c48b5d80e90b6d1443aca4137e6a474fb3660c5932092`
- `api/components/responses.yaml`  
  `c88266b02303eb6b621b7cd6df20385963c2c8ed2864fd84d24e18ae24f93140`
- `api/components/schemas.yaml`  
  `543636cb3d3cdc2ef9ed09dd973a3a65113915917d786f98b3ac5af8d7ab8059`
- `api/components/security_schemes.yaml`  
  `9d45e3181a4b847b617a0553c72458650aa9c3deacf38cbed67c5c12db3e1c79`

### API Specs

- `api/edge_local.v1.yaml`  
  `510fac0f988752927353a6ec0fe431fe0098fbec2600074a39ca96103f040ccd`
- `api/platform_internal.v1.yaml`  
  `63b87780fbd706dd01138391d8e907702cf7044811af82f4e333184b2a82f31c`
- `api/platform_public.v1.yaml`  
  `95c65be2acf30fe5563a5033c978d26457bd53e4b61c80685d287baff4f9b1b5`

---

## Changelog

### v0.0.1 (2026-02-18)

**Breaking:** NO

Version pinned automatically.

---

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

assert verify_contracts("c737c45d0b5b8647b7745587da398a723afba0c4bc98054fc5541c04957e2cc7"), "Contracts checksum mismatch!"
```

### Node.js
```javascript
const crypto = require('crypto');
const assert = require('assert');

function verifyContracts(expectedChecksum) {
  const actualChecksum = computeContractsChecksum();
  return actualChecksum === expectedChecksum;
}

assert(verifyContracts("c737c45d0b5b8647b7745587da398a723afba0c4bc98054fc5541c04957e2cc7"), "Contracts checksum mismatch!");
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

**Last Updated:** 2026-02-18T16:44:58.765180Z

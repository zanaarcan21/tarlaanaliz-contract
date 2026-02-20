# CI Gate Checklist
<!-- BOUND:CI_GATE_CHECKLIST -->

> **Automated CI/CD validation checks** for contract repository

**Build:** #___  
**Branch:** ___  
**Commit:** ___  
**Triggered By:** Push / PR / Manual

---

## 🤖 Automated Checks

All checks run automatically in GitHub Actions workflow: `.github/workflows/contract_validation.yml`

---

## ✅ 1. Schema Validation

### Job: `validate-schemas`

**Script:** `python3 tools/validate.py`

**Checks:**
- [ ] All schemas are valid JSON
- [ ] All schemas use Draft 2020-12
- [ ] All object schemas have `unevaluatedProperties: false`
- [ ] No forbidden fields (email/tckn/otp)
- [ ] Enum values are unique
- [ ] ID patterns follow convention

**Exit Code:** 0 = Pass, 1 = Fail

**Expected Output:**
```
🔍 TarlaAnaliz Contracts Validator

Validating schemas/shared/geojson.v1.schema.json...
Validating schemas/enums/crop_type.enum.v1.json...
...

============================================================
Total files validated: 29
Total errors: 0

✅ ALL VALIDATIONS PASSED
```

**On Failure:**
- [ ] Review validation errors
- [ ] Fix schema issues
- [ ] Re-run validation locally
- [ ] Push fix

---

## 🧪 2. Test Execution

### Job: `test-schemas`

**Script:** `pytest tests/ -v --cov=schemas`

**Test Suites:**
1. **test_validate_all_schemas.py** (20+ tests)
   - [ ] Schema compliance
   - [ ] Draft 2020-12
   - [ ] Forbidden fields
   - [ ] KR-002 compliance (8 crops, 7 layers)
   - [ ] Phone pattern (10 digits)
   - [ ] ID format validation

2. **test_examples_match_schemas.py** (15+ tests)
   - [ ] Examples validate against schemas
   - [ ] Required fields present
   - [ ] KR-002 values used
   - [ ] No forbidden fields
   - [ ] ISO 8601 timestamps

3. **test_no_breaking_changes.py** (10+ tests)
   - [ ] Breaking change detector works
   - [ ] Version bump policy enforced
   - [ ] Semver compliance

**Coverage Target:** >90%

**Expected Output:**
```
============================= test session starts ==============================
tests/test_validate_all_schemas.py::TestSchemaValidation::test_schemas_directory_exists PASSED
tests/test_validate_all_schemas.py::TestSchemaValidation::test_has_schema_files PASSED
...

---------- coverage: platform linux, python 3.11 -----------
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
schemas/                                  ...    ...   95%
-----------------------------------------------------------
TOTAL                                     ...    ...   95%

============================== 40 passed in 2.34s ==============================
```

**On Failure:**
- [ ] Review test failures
- [ ] Fix failing tests or schemas
- [ ] Verify coverage meets threshold
- [ ] Re-run tests locally

---

## 🔍 3. Breaking Change Detection

### Job: `detect-breaking-changes` (PR only)

**Script:** `python3 tools/breaking_change_detector.py --old $BASE --new $HEAD`

**Checks:**
- [ ] Field removals detected
- [ ] Type changes detected
- [ ] Required field additions detected
- [ ] Enum value removals detected
- [ ] Schema removals detected

**Outputs:**
1. **JSON Report:** `breaking_changes.json`
   ```json
   {
     "has_breaking": true,
     "breaking": [...],
     "non_breaking": [...],
     "documentation": [...]
   }
   ```

2. **PR Comment:** Automatically posted to PR

**Expected Behavior:**
- **If breaking changes:** 
  - [ ] Warning posted to PR
  - [ ] MAJOR version bump required
  - [ ] Migration guide required
  - [ ] Does NOT fail build (warning only)

- **If no breaking changes:**
  - [ ] Success comment posted
  - [ ] MINOR/PATCH bump allowed
  - [ ] No migration guide needed

**On Breaking Changes:**
- [ ] Create migration guide
- [ ] Notify consumer teams
- [ ] Plan deprecation timeline
- [ ] Update CONTRACTS_VERSION.md

---

## 🔐 4. Forbidden Field Detection

### Job: `check-forbidden-fields`

**Script:** `grep -r -i -E "\"(email|tckn|otp)\"" schemas/`

**Forbidden Fields:**
- `email`, `e_mail`, `e-mail`
- `tckn`, `tc_kimlik_no`, `tc_no`
- `otp`, `one_time_password`, `verification_code`

**Per KR-050:** NO email, NO TCKN, NO OTP

**Expected Output:**
```
Checking for forbidden fields: email|e_mail|tckn|tc_kimlik_no|otp
✅ No forbidden fields found
```

**Exit Code:** 0 = Pass, 1 = Fail (CRITICAL)

**On Failure:**
- [ ] Forbidden field found
- [ ] **BLOCKS MERGE**
- [ ] Remove forbidden field
- [ ] Use phone + PIN instead

---

## 📜 5. Draft 2020-12 Compliance

### Job: `check-draft-2020-12`

**Script:** `find schemas -name "*.json" -exec grep -L "draft/2020-12" {} \;`

**Check:** All schemas use JSON Schema Draft 2020-12

**Expected Output:**
```
Checking all schemas use Draft 2020-12...
✅ All schemas use Draft 2020-12
```

**Exit Code:** 0 = Pass, 1 = Fail (CRITICAL)

**On Failure:**
- [ ] Schema using wrong draft found
- [ ] **BLOCKS MERGE**
- [ ] Update `$schema` to Draft 2020-12

---

## 🔒 6. Checksum Verification

### Job: `verify-checksums`

**Script:** `python3 tools/pin_version.py --verify`

**Check:** Current schemas match pinned version checksums

**Expected Behavior:**
- **If CONTRACTS_VERSION.md exists:**
  - [ ] Verify SHA-256 hashes match
  - [ ] Pass if match, warn if mismatch
  
- **If CONTRACTS_VERSION.md missing:**
  - [ ] Skip check (not yet pinned)
  - [ ] Continue without error

**On Mismatch:**
- [ ] Schemas changed since last pin
- [ ] Expected after merge (pin after merge)
- [ ] Does NOT block merge

---

## 📝 7. OpenAPI Linting

### Job: `lint-openapi`

**Tool:** Redocly CLI

**Script:** `npm run openapi:validate`

**Checks:**
- [ ] Valid OpenAPI 3.1 syntax
- [ ] Schema references exist
- [ ] No unused components
- [ ] Security schemes defined
- [ ] Response codes appropriate

**Severity Levels:**
- **Error:** Blocks merge
- **Warning:** Logged only
- **Info:** Ignored

**Expected Output:**
```
✔ api/platform_public.v1.yaml
✔ api/platform_internal.v1.yaml
✔ api/edge_local.v1.yaml

No issues found!
```

**On Failure:**
- [ ] Review Redocly errors
- [ ] Fix OpenAPI issues
- [ ] Re-run linter locally

---

## 📊 8. Summary Job

### Job: `summary`

**Purpose:** Aggregate all check results

**Checks:**
- [ ] validate-schemas: ___
- [ ] test-schemas: ___
- [ ] detect-breaking-changes: ___
- [ ] check-forbidden-fields: ___
- [ ] check-draft-2020-12: ___
- [ ] verify-checksums: ___
- [ ] lint-openapi: ___

**Critical Failures:**
If ANY of these fail, **MERGE BLOCKED**:
- ❌ validate-schemas
- ❌ test-schemas
- ❌ check-forbidden-fields
- ❌ check-draft-2020-12

**Non-Critical:**
These can fail without blocking merge:
- ⚠️ detect-breaking-changes (warning only)
- ⚠️ verify-checksums (expected to change)
- ⚠️ lint-openapi (warnings tolerated)

---

## 🔴 Critical Failure Response

### If CI Fails

**Step 1: Identify Failure**
- [ ] Check GitHub Actions tab
- [ ] Review failed job logs
- [ ] Identify specific error

**Step 2: Fix Locally**
```bash
# Run failing check locally
python3 tools/validate.py
pytest tests/ -v
grep -r "email" schemas/

# Fix issues
vim schemas/...

# Verify fix
python3 tools/validate.py
pytest tests/
```

**Step 3: Push Fix**
```bash
git add .
git commit -m "fix: resolve CI validation errors"
git push
```

**Step 4: Wait for Re-run**
- [ ] CI automatically re-runs on push
- [ ] Verify all checks pass
- [ ] Proceed with merge

---

## ⚡ Fast Failure Mode

CI uses **fail-fast: false** for test jobs to run all checks even if one fails.

**Benefits:**
- See all failures at once
- Fix multiple issues in one commit
- Faster iteration

---

## 📈 Performance Targets

| Check | Target Time | Actual |
|-------|-------------|--------|
| Schema Validation | <30s | ___ |
| Test Execution | <2m | ___ |
| Breaking Changes | <1m | ___ |
| Forbidden Fields | <10s | ___ |
| Draft Check | <10s | ___ |
| Total CI Time | <5m | ___ |

**On Timeout:**
- [ ] Check for infinite loops
- [ ] Reduce test parallelism
- [ ] Contact DevOps team

---

## 🔧 Debugging CI Failures

### Common Issues

**Issue: "Module not found"**
```
Fix: Ensure dependencies installed in CI
```

**Issue: "Permission denied"**
```
Fix: chmod +x tools/*.py
```

**Issue: "File not found"**
```
Fix: Check relative paths in scripts
```

**Issue: "Tests timeout"**
```
Fix: Add --timeout flag to pytest
```

---

## 📞 Support

**CI Issues:** #devops-help  
**Test Failures:** #contracts-dev  
**Emergency:** @contracts-on-call

---

## 📋 Manual Validation

To run all CI checks locally:

```bash
# 1. Validation
python3 tools/validate.py

# 2. Tests
pytest tests/ -v --cov=schemas

# 3. Breaking changes
python3 tools/breaking_change_detector.py --old main --new .

# 4. Forbidden fields
grep -r -i "email\|tckn\|otp" schemas/

# 5. Draft 2020-12
grep -L "draft/2020-12" schemas/**/*.json

# 6. Checksums
python3 tools/pin_version.py --verify

# 7. OpenAPI lint
npm run openapi:validate
```

---

**Checklist Version:** 1.0  
**Last Updated:** 2026-01-26  
**CI Workflow:** `.github/workflows/contract_validation.yml`

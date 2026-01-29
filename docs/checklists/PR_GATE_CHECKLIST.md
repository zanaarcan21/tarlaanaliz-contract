# Pull Request Gate Checklist

> **Pre-merge validation checklist** for contract changes

**PR Number:** #___  
**Author:** @___  
**Reviewers:** @___, @___  
**Target Branch:** `main` / `develop`

---

## 📋 PR Information

- [ ] **Title follows convention:** `[type]: brief description`
  - Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
  - Example: `feat: add payroll schema for pilot payments`

- [ ] **Description complete:**
  - [ ] What changed
  - [ ] Why changed
  - [ ] Related KR references
  - [ ] Breaking change flag (if applicable)

- [ ] **Linked issues/tickets:**
  - Resolves: #___
  - Related: #___

---

## ✅ Schema Validation

### 1. JSON Schema Compliance

- [ ] **Run validator:** `python3 tools/validate.py`
  ```bash
  # Expected output: ✅ ALL VALIDATIONS PASSED
  ```

- [ ] **Draft 2020-12:**
  - [ ] All schemas have `$schema` with `draft/2020-12`
  - [ ] No deprecated features used

- [ ] **unevaluatedProperties:**
  - [ ] All `object` types have `unevaluatedProperties: false`
  - [ ] Checked root level and all `$defs`

### 2. Forbidden Fields

- [ ] **NO email/tckn/otp:** Verified no forbidden fields present
  ```bash
  grep -r -i "email\|tckn\|otp" schemas/
  # Expected: No matches
  ```

- [ ] **KR-050 compliance:**
  - [ ] Authentication uses phone + PIN only
  - [ ] PII separated in user_pii.v1.schema.json

### 3. KR-002 Compliance

- [ ] **Crop types:** Only supported crops (if crop_type modified)
  - COTTON, PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, HAZELNUT, OLIVE, RED_LENTIL

- [ ] **Analysis types:** Only 7 map layers (if analysis_type modified)
  - HEALTH, DISEASE, PEST, FUNGUS, WEED, WATER_STRESS, NITROGEN_STRESS

- [ ] **NO prescriptions:** Map layers only, no action recommendations

---

## 🧪 Tests

### 1. Automated Tests

- [ ] **Run all tests:** `pytest tests/ -v`
  ```bash
  # Expected: All tests pass
  ```

- [ ] **Test coverage:**
  - [ ] New schemas have corresponding tests
  - [ ] Modified schemas have updated tests

### 2. Example Validation

- [ ] **Examples updated:** If schema changed, examples updated
- [ ] **Examples validate:** `pytest tests/test_examples_match_schemas.py`
- [ ] **Examples documented:** In `docs/examples/README.md`

### 3. Breaking Change Tests

- [ ] **Run detector:** `python3 tools/breaking_change_detector.py --old main --new .`
- [ ] **Breaking changes documented:** If detected, migration guide created
- [ ] **Version bump correct:** MAJOR if breaking, MINOR if not

---

## 🔄 Breaking Changes

### Detection

- [ ] **Breaking change detector run:**
  ```bash
  python3 tools/breaking_change_detector.py --old main --new . --pr-comment
  ```

- [ ] **Results reviewed:**
  - [ ] Breaking changes: ___
  - [ ] Non-breaking changes: ___

### If Breaking Changes Detected

- [ ] **MAJOR version bump required:** Confirmed
- [ ] **Migration guide created:** `docs/migration_guides/{schema}_v{old}_to_v{new}.md`
- [ ] **Migration guide complete:** All 10 sections filled
- [ ] **Timeline provided:** Deprecation + removal dates
- [ ] **Consumers notified:** Slack #contracts-updates

### If NO Breaking Changes

- [ ] **MINOR version bump:** For new features
- [ ] **PATCH version bump:** For bug fixes/docs

---

## 📝 Documentation

### 1. Schema Documentation

- [ ] **Description complete:** All schemas have description
- [ ] **Field descriptions:** All fields have meaningful descriptions
- [ ] **Examples provided:** Realistic example values

### 2. API Documentation

- [ ] **OpenAPI updated:** If API endpoints changed
- [ ] **Components updated:** If reusable components changed

### 3. Changelog

- [ ] **Entry added:** In CONTRACTS_VERSION.md or CHANGELOG.md
- [ ] **Change type:** Breaking / Feature / Fix
- [ ] **KR referenced:** Related KRs mentioned

---

## 🔐 Security & Compliance

### 1. PII Protection

- [ ] **No PII in schemas:** Except user_pii.v1.schema.json
- [ ] **Phone format:** 10 digits (E.164: +90XXXXXXXXXX)
- [ ] **NO email/TCKN/OTP:** Triple-checked

### 2. Data Integrity

- [ ] **ID format:** All IDs follow `{entity}_{24-char-hex}` pattern
- [ ] **SHA-256 hashes:** For chain-of-custody fields
- [ ] **Timestamps:** ISO 8601 UTC format

### 3. Audit Requirements

- [ ] **Created/updated timestamps:** Present where needed
- [ ] **Actor tracking:** User IDs (NOT PII) for audit trail

---

## 🎨 Code Quality

### 1. Formatting

- [ ] **JSON formatted:** Properly indented (2 spaces)
- [ ] **YAML formatted:** Consistent style
- [ ] **No trailing whitespace**

### 2. Naming Conventions

- [ ] **Schema files:** `{name}.v{version}.schema.json`
- [ ] **Enum files:** `{name}.enum.v{version}.json`
- [ ] **Field names:** snake_case
- [ ] **Enum values:** UPPER_SNAKE_CASE

### 3. Consistency

- [ ] **Patterns match:** Existing schema patterns followed
- [ ] **Types consistent:** Similar fields use same types
- [ ] **References correct:** All `$ref` paths valid

---

## 🔗 Dependencies

### 1. Schema References

- [ ] **Internal refs:** All `$ref` paths exist
- [ ] **Circular refs:** None present (or intentional)
- [ ] **External schemas:** Updated if dependencies changed

### 2. Consumer Impact

- [ ] **Platform service:** Impact assessed
- [ ] **Edge station:** Impact assessed
- [ ] **Worker service:** Impact assessed
- [ ] **Mobile app:** Impact assessed
- [ ] **Web app:** Impact assessed

---

## 📊 Version Management

### 1. Version Pinning

- [ ] **Version determined:**
  - [ ] MAJOR (breaking): x.0.0
  - [ ] MINOR (features): 0.x.0
  - [ ] PATCH (fixes): 0.0.x

- [ ] **Ready to pin:** After merge
  ```bash
  python3 tools/pin_version.py --major|--minor|--patch
  ```

### 2. Checksums

- [ ] **Hash verification:** Post-merge
  ```bash
  python3 tools/pin_version.py --verify
  ```

---

## 👥 Review

### 1. Required Reviewers

- [ ] **Schema owner:** @___
- [ ] **Contracts team:** @contracts-team
- [ ] **Consumer teams:** (if breaking change)
  - [ ] @platform-team
  - [ ] @edge-team
  - [ ] @worker-team

### 2. Review Checklist

- [ ] **Code reviewed:** Logic and structure
- [ ] **Tests reviewed:** Coverage and quality
- [ ] **Docs reviewed:** Completeness and accuracy
- [ ] **Breaking changes reviewed:** If present

---

## 🚀 Pre-Merge

### Final Checks

- [ ] **All CI checks passing:** Green checkmarks
- [ ] **Conflicts resolved:** No merge conflicts
- [ ] **Branch up-to-date:** Rebased on target branch
- [ ] **Approvals received:** Required reviewers approved

### Post-Merge Actions

- [ ] **Pin version:** Run `tools/pin_version.py`
- [ ] **Sync to consumers:** Run `tools/sync_to_repos.sh` (or wait for auto-sync)
- [ ] **Notify teams:** Post in #contracts-updates
- [ ] **Close related issues:** Link in merge commit

---

## ❌ Common Issues

### Validation Failures

**Issue:** `unevaluatedProperties` missing  
**Fix:** Add `"unevaluatedProperties": false` to all object schemas

**Issue:** Forbidden field detected  
**Fix:** Remove email/tckn/otp, use phone + PIN only

**Issue:** Wrong Draft version  
**Fix:** Update `$schema` to `https://json-schema.org/draft/2020-12/schema`

### Test Failures

**Issue:** Example validation fails  
**Fix:** Update example to match new schema

**Issue:** Breaking change not documented  
**Fix:** Create migration guide using template

---

## 📞 Need Help?

- **Validation issues:** #contracts-help
- **Breaking changes:** #contracts-dev
- **Urgent:** @contracts-on-call

---

**Checklist Version:** 1.0  
**Last Updated:** 2026-01-26

---

## Sign-Off

**Author:** I confirm all items checked  
**Signature:** @___ | Date: ___

**Reviewer 1:** Approved  
**Signature:** @___ | Date: ___

**Reviewer 2:** Approved  
**Signature:** @___ | Date: ___
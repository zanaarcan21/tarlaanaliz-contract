# Release Gate Checklist

> **Pre-release validation** for new contract versions

**Version:** v___  
**Release Date:** YYYY-MM-DD  
**Release Manager:** @___  
**Type:** MAJOR / MINOR / PATCH

---

## 📋 Pre-Release Validation

### 1. Version Information

- [ ] **Version determined:**
  - MAJOR: Breaking changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes

- [ ] **Version follows semver:** `X.Y.Z` format

- [ ] **Previous version:** v___

- [ ] **Breaking changes:** YES / NO

---

## ✅ 2. Schema Validation

### All Schemas Pass Validation

- [ ] **Run validator:** `python3 tools/validate.py`
  ```bash
  # Expected: ✅ ALL VALIDATIONS PASSED
  ```

- [ ] **No validation errors**

- [ ] **All tests pass:** `pytest tests/ -v`
  ```bash
  # Expected: All tests passed
  ```

- [ ] **Coverage >90%**

---

## 🔄 3. Breaking Change Review

### If MAJOR Version (Breaking Changes)

- [ ] **Breaking changes documented:**
  ```bash
  python3 tools/breaking_change_detector.py --old v{PREV} --new v{NEW}
  ```

- [ ] **Migration guides created:**
  - [ ] One guide per breaking schema change
  - [ ] All 10 template sections complete
  - [ ] Code examples provided
  - [ ] Timeline with specific dates

- [ ] **Consumer impact assessed:**
  - [ ] Platform service: ___
  - [ ] Edge station: ___
  - [ ] Worker service: ___
  - [ ] Mobile app: ___
  - [ ] Web app: ___

- [ ] **Deprecation timeline established:**
  - [ ] Overlap period: ___ days
  - [ ] Deprecation date: ___
  - [ ] Removal date: ___

### If MINOR/PATCH Version

- [ ] **No breaking changes confirmed**
- [ ] **Backward compatible**
- [ ] **No migration guide needed**

---

## 📝 4. Documentation

### Required Documentation

- [ ] **CONTRACTS_VERSION.md updated:**
  ```bash
  python3 tools/pin_version.py --major|--minor|--patch
  ```

- [ ] **Changelog entry added:**
  - [ ] Version number
  - [ ] Release date
  - [ ] Summary of changes
  - [ ] Breaking change flag
  - [ ] KR references

- [ ] **README.md updated:** If needed

- [ ] **Migration guides linked:** From main README

- [ ] **Examples updated:** All examples validate

### Documentation Quality

- [ ] **All schemas have descriptions**
- [ ] **All fields have descriptions**
- [ ] **Examples are realistic**
- [ ] **No TODO/FIXME comments**

---

## 🔐 5. Security & Compliance

### PII Protection (KR-050)

- [ ] **NO email in any schema**
- [ ] **NO TCKN in any schema**
- [ ] **NO OTP in any schema**
- [ ] **Phone + PIN only**

### KR-002 Compliance

- [ ] **supported crops only:**
  - COTTON, PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, HAZELNUT, OLIVE, RED_LENTIL

- [ ] **7 map layers only:**
  - HEALTH, DISEASE, PEST, FUNGUS, WEED, WATER_STRESS, NITROGEN_STRESS

- [ ] **NO prescriptions:** Map layers only

### Data Integrity

- [ ] **SHA-256 checksums:** All file hashes computed
- [ ] **Checksum verified:** `python3 tools/pin_version.py --verify`
- [ ] **ID format correct:** All IDs follow `{entity}_{24-char-hex}`
- [ ] **Timestamps ISO 8601 UTC**

---

## 🧪 6. Testing

### Automated Tests

- [ ] **All unit tests pass:** 100%
- [ ] **All integration tests pass:** 100%
- [ ] **All example tests pass:** 100%
- [ ] **Breaking change tests pass:** 100%

### Manual Testing

- [ ] **Create test payload:** For each changed schema
- [ ] **Validate payload:** Against new schema
- [ ] **Test API integration:** If API changed
- [ ] **Test type generation:**
  ```bash
  ./tools/generate_types.sh
  # Verify TypeScript & Python types generated
  ```

### Consumer Testing

- [ ] **Platform service:** Tested with new version
- [ ] **Edge station:** Tested with new version
- [ ] **Worker service:** Tested with new version

---

## 🔗 7. Integration Readiness

### Type Generation

- [ ] **TypeScript types generated:**
  ```bash
  ./tools/generate_types.sh --typescript
  # Check: generated/typescript/
  ```

- [ ] **Python types generated:**
  ```bash
  ./tools/generate_types.sh --python
  # Check: generated/python/
  ```

- [ ] **Types validated:** No generation errors

### Consumer Sync

- [ ] **Sync scripts tested:**
  ```bash
  ./tools/sync_to_repos.sh --target platform --verify-only
  ./tools/sync_to_repos.sh --target edge --verify-only
  ./tools/sync_to_repos.sh --target worker --verify-only
  ```

- [ ] **Checksums match:** After sync

---

## 📢 8. Communication

### Pre-Release Communication

- [ ] **Release notes drafted:**
  - What's new
  - What changed
  - Breaking changes
  - Migration guides
  - Timeline

- [ ] **Consumer teams notified:**
  - [ ] Platform team: #platform-dev
  - [ ] Edge team: #edge-dev
  - [ ] Worker team: #worker-dev
  - [ ] Mobile team: #mobile-dev
  - [ ] Web team: #web-dev

- [ ] **Breaking change announcement:** If MAJOR
  - [ ] Email to all teams
  - [ ] Slack announcements
  - [ ] Migration office hours scheduled

### Release Channels

- [ ] **Slack #contracts-updates:** Announcement prepared
- [ ] **Email distribution list:** Draft ready
- [ ] **Internal wiki:** Release page created

---

## 📦 9. Release Artifacts

### Required Files

- [ ] **CONTRACTS_VERSION.md:** Up-to-date with checksums
- [ ] **Changelog:** Complete for this version
- [ ] **Migration guides:** All present (if MAJOR)
- [ ] **Generated types:** TypeScript + Python
- [ ] **README.md:** Version referenced

### Git Tags

- [ ] **Tag created:** `v{VERSION}`
  ```bash
  git tag -a v{VERSION} -m "Release v{VERSION}"
  ```

- [ ] **Tag signed:** (Optional but recommended)

- [ ] **Tag pushed:** To origin

### GitHub Release

- [ ] **Release draft created**
- [ ] **Release notes complete**
- [ ] **Assets uploaded:** (If applicable)
- [ ] **Published:** YES / NO

---

## 🚀 10. Release Execution

### Pre-Release Checklist

- [ ] **All CI checks passing:** Green build
- [ ] **All reviews approved:** Required reviewers signed off
- [ ] **Main branch up-to-date:** No pending PRs
- [ ] **Backup created:** Previous version tagged

### Release Steps

**Step 1: Final Validation**
```bash
# Run all checks one last time
python3 tools/validate.py
pytest tests/ -v
python3 tools/pin_version.py --verify
```

**Step 2: Pin Version**
```bash
# Pin new version
python3 tools/pin_version.py --major  # or --minor/--patch

# Verify
cat CONTRACTS_VERSION.md
```

**Step 3: Commit & Tag**
```bash
git add CONTRACTS_VERSION.md
git commit -m "chore: release v{VERSION}"
git tag -a v{VERSION} -m "Release v{VERSION}"
git push origin main --tags
```

**Step 4: Auto-Sync (Optional)**
```bash
# Trigger auto-sync workflow
# Or manually:
./tools/sync_to_repos.sh --all
```

**Step 5: Publish Release**
- [ ] Create GitHub Release from tag
- [ ] Copy release notes
- [ ] Publish

### Post-Release Verification

- [ ] **Release published:** GitHub Releases page
- [ ] **Tags visible:** `git tag -l`
- [ ] **Auto-sync triggered:** Check GitHub Actions
- [ ] **Consumer PRs created:** (If auto-sync enabled)

---

## 📊 11. Post-Release Monitoring

### First Hour

- [ ] **Monitor consumer PRs:** Check for issues
- [ ] **Watch error rates:** No spike in API errors
- [ ] **Check Slack:** No emergency reports

### First Day

- [ ] **Consumer adoption:** Track migration progress
- [ ] **Support requests:** Answer questions
- [ ] **Bug reports:** Monitor for issues

### First Week

- [ ] **Migration complete:** All consumers updated (if MAJOR)
- [ ] **Deprecation warnings:** Old version usage declining
- [ ] **Performance:** No regression

---

## 🔙 12. Rollback Plan

### Rollback Triggers

- [ ] **Critical bug discovered**
- [ ] **>10% of consumers failing**
- [ ] **Data corruption detected**
- [ ] **Security vulnerability found**

### Rollback Procedure

**Step 1: Immediate (<30 minutes)**
```bash
# Revert release commit
git revert {RELEASE_COMMIT}
git push origin main

# Delete tag
git tag -d v{VERSION}
git push origin :refs/tags/v{VERSION}
```

**Step 2: Notify (<1 hour)**
- [ ] Slack #contracts-emergency
- [ ] Email all consumer teams
- [ ] Update GitHub Release (mark as yanked)

**Step 3: Fix & Re-release (<24 hours)**
- [ ] Root cause analysis
- [ ] Fix issue
- [ ] Add tests
- [ ] Release v{VERSION+1}

---

## ✅ 13. Final Sign-Off

### Release Manager

- [ ] **All checklist items complete**
- [ ] **Documentation up-to-date**
- [ ] **Consumers notified**
- [ ] **Ready for release**

**Signature:** @___ | Date: ___

### Technical Lead

- [ ] **Technical review complete**
- [ ] **Breaking changes acceptable**
- [ ] **Migration path clear**
- [ ] **Approved for release**

**Signature:** @___ | Date: ___

### Product Owner

- [ ] **Business requirements met**
- [ ] **Timeline acceptable**
- [ ] **Risk acceptable**
- [ ] **Approved for release**

**Signature:** @___ | Date: ___

---

## 📞 Emergency Contacts

**Release Issues:**
- Release Manager: @___
- Technical Lead: @___
- On-Call: @contracts-on-call

**Slack Channels:**
- #contracts-emergency (critical)
- #contracts-releases (normal)

**Email:** releases@tarlaanaliz.com

---

## 📈 Release Metrics

**Track:**
- [ ] Time to release: ___
- [ ] Consumer adoption rate: ___%
- [ ] Support requests: ___
- [ ] Bug reports: ___
- [ ] Rollbacks: ___

**Target:**
- Migration complete: <30 days (MAJOR), <7 days (MINOR)
- Zero rollbacks
- <5 support requests

---

**Checklist Version:** 1.0  
**Last Updated:** 2026-01-26

---

## 🎉 Post-Release Celebration

- [ ] **Thank the team:** Shout-outs in #contracts-wins
- [ ] **Document lessons learned:** Add to retro notes
- [ ] **Update runbook:** Improve process for next release
- [ ] **Celebrate:** 🎊

**Release complete! Great work!** 🚀
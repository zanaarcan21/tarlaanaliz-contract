# Migration Guides

> **Version migration documentation** for breaking changes in TarlaAnaliz contracts.

## 📋 Purpose

Migration guides are **mandatory** for all breaking changes (MAJOR version bumps).

They provide:
- **Clear upgrade path** - Step-by-step instructions
- **Consumer impact analysis** - Which services affected
- **Code examples** - Before/after comparisons
- **Testing procedures** - Validation steps
- **Rollback plan** - Emergency recovery

---

## 🎯 When to Create a Migration Guide

### ALWAYS Required

Migration guides are **mandatory** for:

✅ **MAJOR version bumps** (breaking changes)
- Field removal or rename
- Type change
- Required field addition
- Enum value removal
- Schema removal

### NOT Required

Migration guides are **optional** for:

❌ MINOR version bumps (new features)
❌ PATCH version bumps (bug fixes)
❌ Documentation changes

---

## 📝 Writing a Migration Guide

### 1. Use the Template

**Always start with:** `MIGRATION_GUIDE_TEMPLATE.md`

```bash
# Copy template
cp docs/migration_guides/MIGRATION_GUIDE_TEMPLATE.md \
   docs/migration_guides/my_schema_v1_to_v2.md

# Edit
vim docs/migration_guides/my_schema_v1_to_v2.md
```

### 2. Follow Naming Convention

**Format:** `{schema_name}_v{old}_to_v{new}.md`

**Examples:**
- `field_v1_to_v2.md`
- `mission_v2_to_v3.md`
- `analysis_result_v1_to_v2.md`

### 3. Complete All Sections

The template has 10 required sections:

1. **Overview** - What changed and why
2. **Breaking Changes** - Detailed list
3. **Migration Steps** - Numbered instructions
4. **Impact Analysis** - Affected services
5. **Timeline** - Deprecation schedule
6. **Code Examples** - Before/after
7. **Testing** - Validation procedures
8. **Rollback** - Emergency recovery
9. **FAQ** - Common questions
10. **Support** - Contact information

**All sections are mandatory!**

---

## ✅ Migration Guide Checklist

Before submitting a migration guide, verify:

- [ ] Used `MIGRATION_GUIDE_TEMPLATE.md`
- [ ] Filename follows convention: `{schema}_v{old}_to_v{new}.md`
- [ ] All 10 sections completed
- [ ] Breaking changes clearly listed
- [ ] Code examples provided (before/after)
- [ ] Impact analysis complete (all affected services)
- [ ] Timeline with specific dates
- [ ] Testing procedures documented
- [ ] Rollback plan provided
- [ ] Linked from main README
- [ ] Reviewed by at least 2 people

---

## 🎨 Style Guide

### Writing Style

**DO:**
- ✅ Use clear, imperative language: "Update field X", "Change type Y"
- ✅ Provide concrete examples with code
- ✅ Explain WHY changes are needed
- ✅ Include version numbers in examples
- ✅ Show exact error messages

**DON'T:**
- ❌ Use vague language: "Some fields might need updating"
- ❌ Skip examples
- ❌ Assume knowledge
- ❌ Ignore edge cases

### Code Examples

**Always include:**
```markdown
### Before (v1)
\`\`\`json
{
  "old_field": "value"
}
\`\`\`

### After (v2)
\`\`\`json
{
  "new_field": "value"
}
\`\`\`

### Migration Code
\`\`\`python
def migrate_v1_to_v2(old_payload):
    new_payload = old_payload.copy()
    new_payload['new_field'] = old_payload['old_field']
    del new_payload['old_field']
    return new_payload
\`\`\`
```

---

## 📊 Impact Analysis Template

For each breaking change, document:

```markdown
### Change: Field Removal - `deprecated_field`

**Affected Services:**
- ✅ Platform API - Read only (no writes)
- ⚠️  Edge Station - Writes to field (BREAKING)
- ✅ Worker Service - Not used
- ❌ Mobile App - Uses in display (BREAKING)

**Impact Level:** HIGH

**Migration Effort:** 2-3 days
```

---

## 📅 Timeline Template

Always provide specific dates:

```markdown
## Timeline

| Date | Milestone |
|------|-----------|
| 2026-02-01 | v2 contracts released |
| 2026-02-01 - 2026-03-01 | Deprecation period (v1 still supported) |
| 2026-03-01 | v1 deprecated (warnings in logs) |
| 2026-04-01 | v1 removed (v2 required) |

**Current Date:** 2026-01-26  
**Days Until v1 Removal:** 65 days
```

---

## 🔄 Version Support Policy

### Overlap Period

- **MAJOR changes:** 30-day overlap (both versions work)
- **Critical fixes:** 60-day overlap
- **Emergency changes:** Immediate (no overlap)

### Support Matrix

| Version | Status | Support Until |
|---------|--------|---------------|
| v2.x.x | Current | Active |
| v1.x.x | Deprecated | 2026-04-01 |
| v0.x.x | Unsupported | N/A |

---

## 🧪 Testing Requirements

Every migration guide must include:

### 1. Unit Tests
```python
def test_migrate_v1_to_v2():
    v1_payload = {...}
    v2_payload = migrate_v1_to_v2(v1_payload)
    
    # Validate against v2 schema
    Draft202012Validator(v2_schema).validate(v2_payload)
```

### 2. Integration Tests
- Test old payload → new payload conversion
- Test new payload validation
- Test backward compatibility (if overlap period)

### 3. Consumer Tests
- Platform API tests pass with v2
- Edge station tests pass with v2
- Worker service tests pass with v2

---

## 🚨 Emergency Rollback

Every guide must document rollback:

```markdown
## Rollback Procedure

If critical issues discovered:

1. **Immediate:** Revert to v1 contracts
   \`\`\`bash
   git revert <commit-hash>
   git push origin main
   \`\`\`

2. **Within 1 hour:** Notify all consumers
   - Slack: #contracts-emergency
   - Email: platform-team@tarlaanaliz.com

3. **Within 4 hours:** Root cause analysis
   - Document issue in incident report
   - Create hotfix plan

4. **Within 24 hours:** Hotfix deployed
   - Fix issue
   - Create new migration guide
   - Re-release with v2.1
```

---

## 📚 Examples

### Good Migration Guides

✅ **field_v1_to_v2.md** (included in this repo)
- Clear structure
- Complete code examples
- Comprehensive impact analysis
- Realistic timeline
- Tested rollback procedure

### Reference External Examples

For inspiration, see:
- [Stripe API Versioning](https://stripe.com/docs/upgrades)
- [GitHub API Changes](https://docs.github.com/en/rest/overview/api-versions)
- [AWS SDK Migration Guides](https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/migrating-to-v3.html)

---

## 🔗 Integration with Tools

### Automatic Detection

Breaking change detector automatically flags:
```bash
python3 tools/breaking_change_detector.py --old v1.0.0 --new v2.0.0

# Output includes:
# ⚠️  MIGRATION GUIDE REQUIRED
# Expected file: docs/migration_guides/field_v1_to_v2.md
```

### CI Enforcement

CI checks for migration guide:
```yaml
- name: Check migration guide
  if: breaking_changes_detected
  run: |
    # Check guide exists
    test -f docs/migration_guides/${SCHEMA}_v${OLD}_to_v${NEW}.md
```

---

## 📞 Support

### Writing Questions
- **Documentation Team:** Ask in #contracts-docs Slack
- **Template Issues:** Open issue with label `migration-template`

### Technical Questions
- **Schema Changes:** Ask in #contracts-dev Slack
- **Integration Help:** Contact service owners directly

---

## 📋 Quick Reference

### Create New Migration Guide
```bash
# 1. Copy template
cp docs/migration_guides/MIGRATION_GUIDE_TEMPLATE.md \
   docs/migration_guides/my_schema_v1_to_v2.md

# 2. Edit
vim docs/migration_guides/my_schema_v1_to_v2.md

# 3. Complete all sections

# 4. Test
pytest tests/test_migration_guides.py

# 5. Submit PR
git add docs/migration_guides/my_schema_v1_to_v2.md
git commit -m "docs: add migration guide for my_schema v1→v2"
```

### Validate Migration Guide
```bash
# Check all sections present
grep -E "^## (Overview|Breaking Changes|Migration Steps)" \
  docs/migration_guides/my_schema_v1_to_v2.md

# Check examples present
grep -E "^### (Before|After|Migration Code)" \
  docs/migration_guides/my_schema_v1_to_v2.md
```

---

## 📊 Metrics

We track:
- Migration guide completeness (all 10 sections)
- Consumer adoption rate (% migrated in 30 days)
- Rollback incidents (target: 0)
- Time to migrate (target: <7 days)

---

**Last Updated:** 2026-01-26  
**Template Version:** 1.0.0  
**Required for:** MAJOR version bumps only
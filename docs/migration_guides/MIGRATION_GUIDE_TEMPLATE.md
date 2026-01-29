# Migration Guide: [Schema Name] v[OLD] → v[NEW]

> **Migration guide for [Schema Name] breaking changes**

**Version:** v[OLD] → v[NEW]  
**Release Date:** [YYYY-MM-DD]  
**Deprecation Date:** [YYYY-MM-DD]  
**Removal Date:** [YYYY-MM-DD]  
**Author:** [Your Name]  
**Reviewers:** [Reviewer 1], [Reviewer 2]

---

## 1. Overview

### What Changed

[Brief description of what changed and why]

**Example:**
> In v2, we removed the `deprecated_field` and replaced it with `new_field` to improve data consistency and align with KR-XXX requirements.

### Why This Change

[Explanation of business/technical rationale]

**Example:**
> This change was needed because:
> - KR-XXX requires standardized field names
> - `deprecated_field` caused confusion with similar fields
> - `new_field` provides better type safety

### Migration Complexity

**Effort Estimate:** [LOW / MEDIUM / HIGH]  
**Estimated Time:** [X days/weeks]  
**Required Skills:** [e.g., "Backend development, schema validation"]

---

## 2. Breaking Changes

### Change 1: [Change Title]

**Type:** [FIELD_REMOVED / TYPE_CHANGED / FIELD_RENAMED / ENUM_CHANGED]

**Details:**
```diff
- Old behavior: [description]
+ New behavior: [description]
```

**Impact Level:** [LOW / MEDIUM / HIGH / CRITICAL]

**Affected Fields:**
- `field_name` - [description of change]

---

### Change 2: [Change Title]

[Repeat for each breaking change]

---

## 3. Migration Steps

### Prerequisites

Before starting migration:

- [ ] Review all breaking changes above
- [ ] Backup production data
- [ ] Test in staging environment
- [ ] Coordinate with dependent services
- [ ] Schedule maintenance window (if needed)

### Step-by-Step Instructions

#### Step 1: Update Dependencies

```bash
# Update contracts
cd your-repo
git submodule update --remote contracts

# Or sync
cd contracts
./tools/sync_to_repos.sh --target [platform|edge|worker]
```

#### Step 2: Update Schema References

```[language]
# Update import statements
- from contracts.[old_schema_v1] import OldSchema
+ from contracts.[new_schema_v2] import NewSchema
```

#### Step 3: Migrate Data Structures

[Provide specific code for migration]

**Example (Python):**
```python
def migrate_v1_to_v2(v1_payload):
    """Migrate v1 payload to v2 format"""
    v2_payload = v1_payload.copy()
    
    # Change 1: Rename field
    if 'old_field' in v2_payload:
        v2_payload['new_field'] = v2_payload.pop('old_field')
    
    # Change 2: Update type
    if 'count' in v2_payload:
        v2_payload['count'] = str(v2_payload['count'])  # int → string
    
    return v2_payload
```

**Example (TypeScript):**
```typescript
function migrateV1ToV2(v1Payload: V1Schema): V2Schema {
  return {
    ...v1Payload,
    new_field: v1Payload.old_field,
    count: v1Payload.count.toString()
  };
}
```

#### Step 4: Update API Calls

[Show how to update API interactions]

```[language]
# Before (v1)
response = api.post('/fields', old_payload)

# After (v2)
new_payload = migrate_v1_to_v2(old_payload)
response = api.post('/fields', new_payload)
```

#### Step 5: Update Tests

```[language]
# Update test fixtures
def test_field_creation():
    # Before (v1)
    - payload = {'old_field': 'value'}
    
    # After (v2)
    + payload = {'new_field': 'value'}
    
    response = create_field(payload)
    assert response.status == 200
```

#### Step 6: Validate Migration

```bash
# Run validation
pytest tests/ -k "test_v2"

# Validate against schema
python3 -c "
from jsonschema import Draft202012Validator
import json

schema = json.load(open('contracts/schemas/[path]/[schema].v2.schema.json'))
payload = {...}  # Your migrated payload

Draft202012Validator(schema).validate(payload)
print('✅ Valid v2 payload')
"
```

---

## 4. Impact Analysis

### Affected Services

| Service | Impact Level | Action Required | Owner |
|---------|--------------|-----------------|-------|
| Platform API | HIGH | Update handlers | @platform-team |
| Edge Station | MEDIUM | Update ingest | @edge-team |
| Worker Service | LOW | No changes | @worker-team |
| Mobile App | HIGH | Update forms | @mobile-team |
| Web App | HIGH | Update UI | @web-team |

### Data Migration

**Database Changes Required:** [YES / NO]

If YES, provide migration script:

```sql
-- Example SQL migration
ALTER TABLE fields RENAME COLUMN old_field TO new_field;
UPDATE fields SET new_field = old_field WHERE new_field IS NULL;
```

### API Endpoints Affected

| Endpoint | Method | Change |
|----------|--------|--------|
| `/fields` | POST | Request schema updated |
| `/fields/{id}` | GET | Response schema updated |
| `/fields/{id}` | PUT | Request schema updated |

---

## 5. Timeline

| Date | Milestone | Action |
|------|-----------|--------|
| [YYYY-MM-DD] | v[NEW] Release | New schema available |
| [YYYY-MM-DD] | Migration Start | Begin updating services |
| [YYYY-MM-DD] | Deprecation Notice | v[OLD] marked deprecated |
| [YYYY-MM-DD] | Migration Deadline | All services must use v[NEW] |
| [YYYY-MM-DD] | v[OLD] Removal | v[OLD] no longer supported |

**Current Date:** [YYYY-MM-DD]  
**Days Remaining:** [X days]

### Deprecation Period

**Duration:** [X days] overlap period

During deprecation:
- Both v[OLD] and v[NEW] supported
- v[OLD] logs deprecation warnings
- No new features for v[OLD]
- Bug fixes only for critical issues

---

## 6. Code Examples

### Example 1: Basic Migration

**Before (v1):**
```json
{
  "field_id": "field_abc123",
  "old_field": "value",
  "deprecated_type": "OLD_TYPE"
}
```

**After (v2):**
```json
{
  "field_id": "field_abc123",
  "new_field": "value",
  "type": "NEW_TYPE"
}
```

**Migration Code (Python):**
```python
from contracts.schema_v1 import SchemaV1
from contracts.schema_v2 import SchemaV2

def migrate_to_v2(v1_data: SchemaV1) -> SchemaV2:
    return SchemaV2(
        field_id=v1_data.field_id,
        new_field=v1_data.old_field,
        type=convert_type(v1_data.deprecated_type)
    )

def convert_type(old_type: str) -> str:
    mapping = {
        'OLD_TYPE': 'NEW_TYPE',
        # Add more mappings
    }
    return mapping.get(old_type, 'DEFAULT_TYPE')
```

### Example 2: Batch Migration

**Migrate Multiple Records:**
```python
def migrate_batch(v1_records: list[dict]) -> list[dict]:
    """Migrate batch of v1 records to v2"""
    v2_records = []
    errors = []
    
    for i, v1_record in enumerate(v1_records):
        try:
            v2_record = migrate_v1_to_v2(v1_record)
            
            # Validate
            Draft202012Validator(v2_schema).validate(v2_record)
            
            v2_records.append(v2_record)
        except Exception as e:
            errors.append({
                'index': i,
                'record_id': v1_record.get('field_id'),
                'error': str(e)
            })
    
    return v2_records, errors
```

### Example 3: API Client Update

**Before (v1 Client):**
```typescript
class FieldClient {
  async createField(data: FieldV1): Promise<Response> {
    return this.api.post('/fields', data);
  }
}
```

**After (v2 Client):**
```typescript
class FieldClient {
  async createField(data: FieldV2): Promise<Response> {
    // Optionally support v1 data with auto-migration
    const v2Data = this.isV1(data) 
      ? this.migrateV1ToV2(data) 
      : data;
    
    return this.api.post('/fields', v2Data);
  }
  
  private migrateV1ToV2(v1: FieldV1): FieldV2 {
    return {
      ...v1,
      new_field: v1.old_field,
      // ... other migrations
    };
  }
}
```

---

## 7. Testing

### Unit Tests

```python
# test_migration.py

def test_migrate_v1_to_v2_basic():
    """Test basic field migration"""
    v1 = {
        'field_id': 'field_123',
        'old_field': 'test',
        'deprecated_type': 'OLD'
    }
    
    v2 = migrate_v1_to_v2(v1)
    
    assert v2['field_id'] == 'field_123'
    assert v2['new_field'] == 'test'
    assert v2['type'] == 'NEW'
    assert 'old_field' not in v2

def test_migrate_preserves_other_fields():
    """Test migration preserves unaffected fields"""
    v1 = {
        'field_id': 'field_123',
        'old_field': 'test',
        'unchanged_field': 'keep_this'
    }
    
    v2 = migrate_v1_to_v2(v1)
    
    assert v2['unchanged_field'] == 'keep_this'

def test_migrate_validates_against_schema():
    """Test migrated data validates against v2 schema"""
    v1 = create_valid_v1_payload()
    v2 = migrate_v1_to_v2(v1)
    
    # Should not raise
    Draft202012Validator(v2_schema).validate(v2)
```

### Integration Tests

```python
def test_api_accepts_migrated_payload():
    """Test API accepts migrated v2 payload"""
    v1_payload = {...}
    v2_payload = migrate_v1_to_v2(v1_payload)
    
    response = api_client.post('/fields', json=v2_payload)
    
    assert response.status_code == 201
    assert response.json()['field_id']
```

### Manual Testing Checklist

- [ ] Create new record with v2 schema
- [ ] Update existing record migrated from v1
- [ ] Read migrated record
- [ ] Delete migrated record
- [ ] Test all affected API endpoints
- [ ] Verify UI displays correctly
- [ ] Check logs for errors
- [ ] Validate against v2 schema

---

## 8. Rollback Procedure

### When to Rollback

Trigger rollback if:
- Critical bugs discovered in v2
- >10% of API calls failing
- Data corruption detected
- Consumer services unable to migrate in time

### Rollback Steps

#### Immediate Rollback (<1 hour)

```bash
# 1. Revert contracts
cd tarlaanaliz-contracts
git revert [commit-hash]
git push origin main

# 2. Notify consumers
# Send to: #contracts-emergency Slack
# Message: "v2 rolled back due to [issue]. Reverting to v1."

# 3. Redeploy services with v1
./deploy.sh --version v1
```

#### Post-Rollback (<24 hours)

1. **Root Cause Analysis**
   - Document issue
   - Identify what went wrong
   - Create incident report

2. **Fix and Re-release**
   - Fix issue in v2.1
   - Add additional tests
   - Create new migration guide
   - Re-release with longer deprecation period

### Rollback Impact

| Service | Rollback Action | Data Loss Risk |
|---------|----------------|----------------|
| Platform API | Redeploy v1 | None (if <1 hour) |
| Edge Station | Revert config | None |
| Worker Service | No action | None |

---

## 9. FAQ

### Q: Can I continue using v1 after the deadline?

**A:** No. After [REMOVAL_DATE], v1 will return 410 Gone errors. You must migrate before the deadline.

### Q: What if my service isn't ready by the deadline?

**A:** Contact @contracts-team ASAP. We may extend deprecation period for critical services.

### Q: Can I use both v1 and v2 during migration?

**A:** Yes, during the deprecation period ([START] - [END]), both versions are supported.

### Q: What happens to existing v1 data?

**A:** [Describe data migration strategy]

### Q: How do I know if migration was successful?

**A:** Run the validation script:
```bash
python3 scripts/validate_v2_migration.py
```

### Q: Where can I get help?

**A:** See Support section below.

---

## 10. Support

### Getting Help

**General Questions:**
- Slack: #contracts-help
- Email: contracts@tarlaanaliz.com

**Technical Issues:**
- Slack: #contracts-dev
- Create issue: [GitHub Issues](https://github.com/tarlaanaliz/contracts/issues)

**Emergency (Production Down):**
- Slack: #contracts-emergency
- On-call: +90 XXX XXX XXXX

### Office Hours

**Migration Support:** Every Tuesday 14:00-16:00 UTC
- Join: [Zoom Link]
- No appointment needed

### Resources

- [Main Documentation](../../README.md)
- [Schema Reference](../../schemas/)
- [API Documentation](../../api/)
- [Breaking Change Policy](../../versioning_policy.md)

---

## Appendix

### A. Complete Field Mapping

| v1 Field | v2 Field | Transformation | Notes |
|----------|----------|----------------|-------|
| `old_field` | `new_field` | Direct rename | No data change |
| `deprecated_type` | `type` | Value mapping | See convert_type() |
| [Add all fields] | | | |

### B. Error Messages

Common errors during migration:

**Error:** `ValidationError: 'new_field' is required`  
**Fix:** Ensure all v1 `old_field` values are migrated to `new_field`

**Error:** `Invalid enum value for 'type'`  
**Fix:** Use convert_type() mapping function

### C. Migration Script

Complete migration script available at:
`scripts/migrate_[schema]_v1_to_v2.py`

---

**Document Version:** 1.0  
**Last Updated:** [YYYY-MM-DD]  
**Next Review:** [YYYY-MM-DD]
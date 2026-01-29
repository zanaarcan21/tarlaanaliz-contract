# Migration Guide: Field Schema v1 → v2

> **Example migration guide (for template validation)**

**Version:** v1.0.0 → v2.0.0  
**Release Date:** 2026-02-01  
**Deprecation Date:** 2026-03-01  
**Removal Date:** 2026-04-01  
**Author:** TarlaAnaliz Contracts Team  
**Reviewers:** Platform Team, Edge Team

---

## 1. Overview

### What Changed

In Field v2, we've made three breaking changes:

1. **Renamed field:** `crop_season` → `season` (better naming)
2. **Type change:** `area_donum` from `integer` → `number` (decimal precision)
3. **New required field:** `registration_source` (audit requirement)

### Why This Change

These changes were needed to:
- **KR-013 Compliance:** Registration source tracking required for audit
- **Precision:** Donum measurements need decimal precision (e.g., 25.5 donum)
- **Consistency:** Align field naming with other schemas

### Migration Complexity

**Effort Estimate:** MEDIUM  
**Estimated Time:** 2-3 days  
**Required Skills:** Backend development, schema validation

---

## 2. Breaking Changes

### Change 1: Field Rename

**Type:** FIELD_RENAMED

**Details:**
```diff
- Old field: "crop_season"
+ New field: "season"
```

**Impact Level:** LOW

**Affected Fields:**
- `crop_season` → renamed to `season`, structure unchanged

### Change 2: Type Change

**Type:** TYPE_CHANGED

**Details:**
```diff
- Old type: "area_donum": { "type": "integer" }
+ New type: "area_donum": { "type": "number" }
```

**Impact Level:** MEDIUM

**Rationale:** Donum measurements need decimal precision. Integer truncation caused data loss.

### Change 3: New Required Field

**Type:** FIELD_ADDED_REQUIRED

**Details:**
```diff
+ New required field: "registration_source"
+ Values: "WEB_APP", "MOBILE_APP", "COOP_IMPORT", "ADMIN_TOOL"
```

**Impact Level:** HIGH

**Rationale:** KR-013 requires tracking how fields were registered for audit purposes.

---

## 3. Migration Steps

### Prerequisites

Before starting migration:

- [x] Review all breaking changes above
- [x] Backup production database
- [x] Test in staging environment
- [x] Coordinate with platform and edge teams
- [ ] Schedule maintenance window: 2026-02-01 02:00-04:00 UTC

### Step-by-Step Instructions

#### Step 1: Update Contracts Submodule

```bash
# In your service repository
cd your-service
git submodule update --remote contracts

# Verify version
cd contracts
grep "Version:" CONTRACTS_VERSION.md
# Should show: Version: 2.0.0
```

#### Step 2: Update Schema References

**Python:**
```python
# Before
from contracts.field_v1 import Field as FieldV1

# After
from contracts.field_v2 import Field as FieldV2
```

**TypeScript:**
```typescript
// Before
import { Field as FieldV1 } from './contracts/field.v1';

// After
import { Field as FieldV2 } from './contracts/field.v2';
```

#### Step 3: Implement Migration Function

**Python Example:**
```python
def migrate_field_v1_to_v2(v1_field: dict) -> dict:
    """Migrate field from v1 to v2 schema"""
    v2_field = v1_field.copy()
    
    # Change 1: Rename crop_season → season
    if 'crop_season' in v2_field:
        v2_field['season'] = v2_field.pop('crop_season')
    
    # Change 2: Ensure area_donum is decimal
    if 'area_donum' in v2_field:
        v2_field['area_donum'] = float(v2_field['area_donum'])
    
    # Change 3: Add registration_source (default to unknown)
    if 'registration_source' not in v2_field:
        # Try to infer from metadata
        v2_field['registration_source'] = infer_source(v2_field)
    
    return v2_field

def infer_source(field: dict) -> str:
    """Infer registration source from field metadata"""
    # Check created_by user role
    if field.get('created_by_role') == 'COOP_ADMIN':
        return 'COOP_IMPORT'
    elif field.get('created_via') == 'mobile':
        return 'MOBILE_APP'
    elif field.get('created_via') == 'admin':
        return 'ADMIN_TOOL'
    else:
        return 'WEB_APP'  # Default
```

**TypeScript Example:**
```typescript
function migrateFieldV1ToV2(v1Field: FieldV1): FieldV2 {
  return {
    ...v1Field,
    season: v1Field.crop_season,  // Rename
    area_donum: parseFloat(v1Field.area_donum.toString()),  // To decimal
    registration_source: inferSource(v1Field)  // Add required field
  };
}

function inferSource(field: FieldV1): RegistrationSource {
  if (field.created_by_role === 'COOP_ADMIN') {
    return 'COOP_IMPORT';
  } else if (field.created_via === 'mobile') {
    return 'MOBILE_APP';
  } else if (field.created_via === 'admin') {
    return 'ADMIN_TOOL';
  } else {
    return 'WEB_APP';
  }
}
```

#### Step 4: Update Database (if applicable)

```sql
-- Migration for PostgreSQL

-- 1. Rename column
ALTER TABLE fields RENAME COLUMN crop_season TO season;

-- 2. Change type (area_donum: integer → decimal)
ALTER TABLE fields 
  ALTER COLUMN area_donum TYPE NUMERIC(10,2);

-- 3. Add registration_source
ALTER TABLE fields 
  ADD COLUMN registration_source VARCHAR(20) NOT NULL DEFAULT 'WEB_APP';

-- 4. Update registration_source based on audit data
UPDATE fields 
SET registration_source = 
  CASE 
    WHEN created_by_role = 'COOP_ADMIN' THEN 'COOP_IMPORT'
    WHEN created_via = 'mobile' THEN 'MOBILE_APP'
    WHEN created_via = 'admin' THEN 'ADMIN_TOOL'
    ELSE 'WEB_APP'
  END;

-- 5. Remove default
ALTER TABLE fields 
  ALTER COLUMN registration_source DROP DEFAULT;
```

#### Step 5: Update API Handlers

**Example (FastAPI):**
```python
from contracts.field_v2 import Field as FieldV2

@app.post("/fields")
async def create_field(field: FieldV2):
    # Validate (automatic with Pydantic)
    # field is already validated against v2 schema
    
    # Save to database
    db_field = await db.fields.insert_one(field.dict())
    
    return {"field_id": str(db_field.inserted_id)}

# Optional: Support v1 with auto-migration
@app.post("/fields/legacy")
async def create_field_v1(field: FieldV1):
    # Migrate to v2
    field_v2 = migrate_field_v1_to_v2(field.dict())
    
    # Use v2 endpoint
    return await create_field(FieldV2(**field_v2))
```

#### Step 6: Update Tests

```python
def test_field_creation_v2():
    """Test field creation with v2 schema"""
    field_data = {
        "field_id": "field_507f1f77bcf86cd799439011",
        "name": "Test Field",
        "boundary": {...},
        "area_hectares": 10.5,
        "area_donum": 105.5,  # Now decimal!
        "crop_type": "COTTON",
        "season": {  # Renamed from crop_season
            "year": 2026,
            "season_type": "SPRING"
        },
        "registration_source": "WEB_APP",  # New required field
        "location": {...}
    }
    
    # Validate
    from jsonschema import Draft202012Validator
    schema = load_schema('field.v2.schema.json')
    Draft202012Validator(schema).validate(field_data)
    
    # Create
    response = client.post('/fields', json=field_data)
    assert response.status_code == 201

def test_migration_v1_to_v2():
    """Test migration function"""
    v1_data = {
        "field_id": "field_123",
        "crop_season": {"year": 2026},  # Old name
        "area_donum": 105,  # Integer
        # registration_source missing
    }
    
    v2_data = migrate_field_v1_to_v2(v1_data)
    
    assert "season" in v2_data
    assert "crop_season" not in v2_data
    assert isinstance(v2_data["area_donum"], float)
    assert "registration_source" in v2_data
```

---

## 4. Impact Analysis

### Affected Services

| Service | Impact Level | Action Required | Owner | Status |
|---------|--------------|-----------------|-------|--------|
| Platform API | HIGH | Update handlers, DB migration | @platform-team | In Progress |
| Edge Station | MEDIUM | Update field creation | @edge-team | Not Started |
| Worker Service | LOW | Read-only (no changes) | @worker-team | Complete |
| Mobile App | HIGH | Update forms, add dropdown | @mobile-team | Not Started |
| Web App | HIGH | Update forms, add dropdown | @web-team | In Progress |

### Data Migration

**Database Changes Required:** YES

**Migration Script:** See Step 4 above

**Estimated Downtime:** 2 hours (during maintenance window)

**Data at Risk:** None (backward compatible migration)

### API Endpoints Affected

| Endpoint | Method | Change | Backward Compatible |
|----------|--------|--------|---------------------|
| `/fields` | POST | Request schema v2 | No |
| `/fields` | GET | Response schema v2 | Yes (added fields) |
| `/fields/{id}` | GET | Response schema v2 | Yes |
| `/fields/{id}` | PUT | Request schema v2 | No |

---

## 5. Timeline

| Date | Milestone | Action |
|------|-----------|--------|
| 2026-02-01 | v2.0.0 Release | New schema available in contracts repo |
| 2026-02-01 | Migration Start | Platform team begins DB migration |
| 2026-02-08 | Edge Updated | Edge station using v2 |
| 2026-02-15 | Apps Updated | Mobile & web apps using v2 |
| 2026-03-01 | Deprecation Notice | v1 marked deprecated (logs warnings) |
| 2026-04-01 | v1 Removal | v1 endpoints return 410 Gone |

**Current Date:** 2026-01-26  
**Days Until v1 Removal:** 65 days

### Deprecation Period

**Duration:** 60 days overlap period (2026-02-01 to 2026-04-01)

During deprecation:
- Both v1 and v2 endpoints supported
- v1 endpoints log deprecation warnings
- No new features for v1
- Security patches only for v1

---

## 6. Code Examples

### Example 1: Basic Field Creation

**Before (v1):**
```json
{
  "field_id": "field_507f1f77bcf86cd799439011",
  "name": "Güneydoğu Tarlası",
  "crop_season": {
    "year": 2026,
    "season_type": "SPRING"
  },
  "area_donum": 105,
  "crop_type": "COTTON"
}
```

**After (v2):**
```json
{
  "field_id": "field_507f1f77bcf86cd799439011",
  "name": "Güneydoğu Tarlası",
  "season": {
    "year": 2026,
    "season_type": "SPRING"
  },
  "area_donum": 105.5,
  "crop_type": "COTTON",
  "registration_source": "WEB_APP"
}
```

### Example 2: Edge Station Integration

**Python (Edge Station):**
```python
from contracts.field_v2 import Field

def create_field_from_card(card_data: dict) -> str:
    """Create field from memory card data"""
    field = Field(
        name=card_data['field_name'],
        boundary=card_data['gps_boundary'],
        area_hectares=card_data['area_ha'],
        area_donum=card_data['area_donum'],
        crop_type=card_data['crop'],
        season={
            'year': 2026,
            'season_type': 'SPRING',
            'planting_date': card_data['planting_date']
        },
        registration_source='EDGE_STATION',  # New field
        location=parse_location(card_data)
    )
    
    # Send to platform
    response = platform_api.post('/fields', field.dict())
    return response.json()['field_id']
```

---

## 7. Testing

### Automated Tests

```bash
# Run migration tests
pytest tests/test_field_migration_v1_to_v2.py -v

# Expected output:
# ✅ test_migrate_renames_crop_season
# ✅ test_migrate_converts_area_donum_to_decimal
# ✅ test_migrate_adds_registration_source
# ✅ test_migrate_validates_against_v2_schema
# ✅ test_api_accepts_v2_payload
```

### Manual Testing Checklist

- [ ] Create new field via web app
- [ ] Create new field via mobile app
- [ ] Import fields via coop bulk upload
- [ ] Migrate existing v1 field to v2
- [ ] Read field (GET /fields/{id})
- [ ] Update field (PUT /fields/{id})
- [ ] List fields (GET /fields)
- [ ] Verify decimals display correctly
- [ ] Check registration_source in admin panel

---

## 8. Rollback Procedure

### Trigger Conditions

Rollback if:
- Database migration fails
- >5% of field creations failing
- Data corruption detected
- Critical bug in v2 schema

### Rollback Steps

```bash
# 1. Immediate rollback (<30 minutes)
cd tarlaanaliz-contracts
git revert abc123  # v2 release commit
git push origin main

# 2. Database rollback
psql -U postgres tarlaanaliz < backups/fields_pre_v2_migration.sql

# 3. Redeploy services
kubectl rollout undo deployment/platform-api
kubectl rollout undo deployment/edge-service

# 4. Notify teams
# Slack: #contracts-emergency
# "Field v2 rolled back. Reverted to v1. Investigation ongoing."
```

### Rollback Impact

- No data loss (if rollback <1 hour)
- v2 fields created during window will be migrated back to v1 format
- registration_source data preserved in audit log

---

## 9. FAQ

### Q: Why decimal instead of integer for area_donum?

**A:** Farmers often have fractional donum (e.g., 25.5 donum). Integer truncation caused data loss.

### Q: Can I leave registration_source empty?

**A:** No, it's required in v2. Use inference function or set to 'WEB_APP' as default.

### Q: What if I created fields before v2?

**A:** During migration, we'll infer registration_source from audit logs. Default is 'WEB_APP'.

### Q: Do I need to update all fields immediately?

**A:** No. Fields are migrated on-read. First GET after 2026-02-01 migrates automatically.

---

## 10. Support

### Getting Help

**General Questions:**
- Slack: #contracts-help
- Email: contracts@tarlaanaliz.com

**Migration Issues:**
- Slack: #field-v2-migration (temporary channel)
- Office Hours: Tuesday 14:00-16:00 UTC

**Emergency:**
- Slack: #contracts-emergency
- On-call: Contracts Team rotation

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-26
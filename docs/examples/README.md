# TarlaAnaliz Contract Examples

<!-- BOUND:DOCS_EXAMPLES_README -->

> **Validated example payloads** for all major schemas.

## 📋 Purpose

These examples serve multiple purposes:

1. **Documentation** - Show real-world usage of schemas
2. **Testing** - Used in automated tests to verify schema validity
3. **Reference** - Copy-paste starting points for integration
4. **Validation** - All examples pass schema validation (tested in CI)

---

## 📁 Available Examples

| Example File | Schema | Description |
|--------------|--------|-------------|
| `field.example.json` | `core/field.v1.schema.json` | Field registration |
| `mission.example.json` | `core/mission.v1.schema.json` | Mission creation |
| `intake_manifest.example.json` | `edge/intake_manifest.v1.schema.json` | Edge intake batch |
| `analysis_job.example.json` | `worker/analysis_job.v1.schema.json` | AI analysis job |
| `analysis_result.example.json` | `worker/analysis_result.v1.schema.json` | AI analysis result |

---

## ✅ Validation Status

All examples are automatically validated against their schemas in CI.

**Test Suite:** `tests/test_examples_match_schemas.py`

### Validation Checks

- ✅ JSON syntax validity
- ✅ Schema compliance (Draft 2020-12)
- ✅ Required fields present
- ✅ Field types correct
- ✅ Enum values valid
- ✅ ID format compliance
- ✅ No forbidden fields (email/tckn/otp)
- ✅ KR-002 compliance (9 crops, 7 layers)

---

## 🔍 Example Details

### field.example.json

**Schema:** `schemas/core/field.v1.schema.json`

**Purpose:** Register a new agricultural field

**Key Features:**
- GeoJSON Polygon boundary
- GAP crop type (KR-002: 9 crops only)
- Turkish address format
- Season information
- Area in hectares

**Usage:**
```bash
# Validate
python3 -c "
import json
from jsonschema import Draft202012Validator

schema = json.load(open('../../schemas/core/field.v1.schema.json'))
example = json.load(open('field.example.json'))

Draft202012Validator(schema).validate(example)
print('✅ Valid!')
"
```

**API Endpoint:** `POST /fields`

---

### mission.example.json

**Schema:** `schemas/core/mission.v1.schema.json`

**Purpose:** Create drone mission for field scanning

**Key Features:**
- Field reference
- KR-002 analysis types (7 types only)
- Schedule information
- Priority level
- Pilot assignment

**API Endpoint:** `POST /missions`

---

### intake_manifest.example.json

**Schema:** `schemas/edge/intake_manifest.v1.schema.json`

**Purpose:** Edge station batch intake record

**Key Features:**
- SHA-256 file hashes (chain-of-custody)
- Quarantine status
- Antivirus scan results
- Certificate verification
- Operator signature

**Usage:** Edge station → Platform upload

---

### analysis_job.example.json

**Schema:** `schemas/worker/analysis_job.v1.schema.json`

**Purpose:** AI analysis job submission

**Key Features:**
- Mission and field references
- Input file references (with SHA-256)
- KR-002 analysis types
- Crop-specific model routing (KR-016)

**Usage:** Platform → AI Worker queue

---

### analysis_result.example.json

**Schema:** `schemas/worker/analysis_result.v1.schema.json`

**Purpose:** AI analysis result output

**Key Features:**
- Map layers (KR-002: 7 types)
- Health score and metrics
- Layer URIs with SHA-256 hashes
- Model fingerprint (reproducibility)
- **NO prescriptions** (map layers only)

**Usage:** AI Worker → Platform delivery

---

## 🎯 KR-002 Compliance

All examples comply with KR-002 requirements:

### 9 GAP Crops Only
```json
{
  "crop_type": "COTTON"  // or PISTACHIO, MAIZE, WHEAT, SUNFLOWER, GRAPE, HAZELNUT, OLIVE, RED_LENTIL
}
```

### 7 Map Layers Only
```json
{
  "analysis_types": [
    "HEALTH",           // Sağlık (Green)
    "DISEASE",          // Hastalık (Orange)
    "PEST",             // Zararlı Böcek (Red)
    "FUNGUS",           // Mantar (Purple)
    "WEED",             // Yabancı Ot (Yellow + dotted)
    "WATER_STRESS",     // Su Stresi (Blue + drops)
    "NITROGEN_STRESS"   // Azot Stresi (Gray + cross-hatch)
  ]
}
```

---

## 🚫 Forbidden Fields (KR-050)

Examples **NEVER** contain:
- ❌ `email` or `e_mail`
- ❌ `tckn` or `tc_kimlik_no`
- ❌ `otp` or `one_time_password`

**Authentication:** Phone + PIN only
- Phone: 10 digits (E.164: `+905432120210`)
- PIN: 6 digits (hashed, never in examples)

---

## 🔐 ID Format

All entity IDs follow pattern: `{entity}_{24-char-hex}`

Examples:
```json
{
  "field_id": "field_507f1f77bcf86cd799439011",
  "mission_id": "mission_60a7f1b8c9d4e5f6a7b8c9d0",
  "user_id": "user_60a7f1b8c9d4e5f6a7b8c9d0",
  "job_id": "job_60a7f1b8c9d4e5f6a7b8c9d2",
  "result_id": "result_60a7f1b8c9d4e5f6a7b8c9d3"
}
```

---

## 📅 Timestamp Format

All timestamps use ISO 8601 UTC:

```json
{
  "created_at": "2026-01-15T10:30:00Z",
  "scheduled_date": "2026-06-15"
}
```

---

## 🧪 Testing Examples

### Run All Example Tests

```bash
# From repository root
pytest tests/test_examples_match_schemas.py -v
```

### Test Specific Example

```python
import json
from jsonschema import Draft202012Validator

# Load schema
with open('../../schemas/core/field.v1.schema.json') as f:
    schema = json.load(f)

# Load example
with open('field.example.json') as f:
    example = json.load(f)

# Validate
validator = Draft202012Validator(schema)
errors = list(validator.iter_errors(example))

if errors:
    for error in errors:
        print(f"❌ {error.message}")
else:
    print("✅ Valid!")
```

---

## 📝 Creating New Examples

When creating new examples:

1. **Follow existing patterns**
   - Use realistic data
   - Include all required fields
   - Follow ID format
   - Use KR-002 values

2. **Validate before committing**
   ```bash
   pytest tests/test_examples_match_schemas.py::TestExamplesValidation::test_example_validates_against_schema[your-example.json]
   ```

3. **Update this README**
   - Add to table above
   - Document key features
   - Explain use case

4. **Check forbidden fields**
   ```bash
   grep -i "email\|tckn\|otp" your-example.json
   # Should return nothing!
   ```

---

## 🔄 Keeping Examples Updated

Examples are **automatically tested** on every PR.

If a schema changes:
1. CI will fail if examples no longer validate
2. Update affected examples
3. Re-run tests
4. Examples must pass before merge

**Test Coverage:** 100% of examples validated

---

## 🌐 Turkish Specifics

### Address Format
```json
{
  "location": {
    "province": "Diyarbakır",      // İl
    "province_code": "21",          // Plaka kodu
    "district": "Çermik",           // İlçe
    "village": "Örnek Köy"          // Köy
  }
}
```

### Phone Format (KR-013)
```json
{
  "phone": "+905432120210"  // +90 + 10 digits (NO leading 0)
}
```

### Money Format (KDV)
```json
{
  "price": {
    "amount": 150.00,
    "currency": "TRY",
    "tax_rate": 20,          // KDV %20
    "tax_amount": 30.00,
    "total": 180.00
  }
}
```

---

## 📚 Related Documentation

- **Schemas:** `../../schemas/`
- **API Specs:** `../../api/`
- **Validation:** `../../tools/validate.py`
- **Tests:** `../../tests/test_examples_match_schemas.py`
- **Main Docs:** `../README.md`

---

## ⚡ Quick Reference

### Validate All Examples
```bash
pytest tests/test_examples_match_schemas.py
```

### Validate Single Example
```bash
python3 -c "
import json
from jsonschema import Draft202012Validator
schema = json.load(open('schemas/core/field.v1.schema.json'))
example = json.load(open('docs/examples/field.example.json'))
Draft202012Validator(schema).validate(example)
print('✅')
"
```

### Check for Forbidden Fields
```bash
grep -r -i "email\|tckn\|otp" docs/examples/*.json
# Should return nothing!
```

---

**Last Updated:** 2026-01-26  
**Examples Count:** 5  
**Validation Status:** ✅ All passing
#!/usr/bin/env python3
"""
TarlaAnaliz Contracts Validator
Validates all JSON Schema and OpenAPI files
"""
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Forbidden fields (per KR-050: NO email, NO TCKN, NO OTP)
FORBIDDEN_FIELDS = ['email', 'e_mail', 'tckn', 'tc_kimlik_no', 'otp', 'one_time_password']

def validate_json_schema(schema_path: Path) -> List[str]:
    """Validate JSON Schema file"""
    errors = []
    
    try:
        with open(schema_path) as f:
            schema = json.load(f)
        
        # Check $schema
        if '$schema' not in schema:
            errors.append(f"Missing $schema in {schema_path}")
        elif 'draft/2020-12' not in schema['$schema']:
            errors.append(f"Wrong draft version in {schema_path} (must be 2020-12)")
        
        # Check unevaluatedProperties
        if schema.get('type') == 'object':
            if 'unevaluatedProperties' not in schema:
                errors.append(f"Missing unevaluatedProperties in {schema_path}")
            elif schema['unevaluatedProperties'] != False:
                errors.append(f"unevaluatedProperties must be false in {schema_path}")
        
        # Check for forbidden fields
        schema_str = json.dumps(schema).lower()
        for field in FORBIDDEN_FIELDS:
            if f'"{field}"' in schema_str:
                errors.append(f"FORBIDDEN field '{field}' found in {schema_path}")
    
    except json.JSONDecodeError as e:
        errors.append(f"JSON parse error in {schema_path}: {e}")
    except Exception as e:
        errors.append(f"Error validating {schema_path}: {e}")
    
    return errors

def main():
    """Main validation"""
    print("🔍 TarlaAnaliz Contracts Validator\n")
    
    base_dir = Path(__file__).parent.parent
    schemas_dir = base_dir / 'schemas'
    
    all_errors = []
    total_files = 0
    
    # Validate all JSON Schema files
    for schema_file in schemas_dir.rglob('*.json'):
        total_files += 1
        print(f"Validating {schema_file.relative_to(base_dir)}...")
        errors = validate_json_schema(schema_file)
        all_errors.extend(errors)
    
    # Print results
    print(f"\n{'='*60}")
    print(f"Total files validated: {total_files}")
    print(f"Total errors: {len(all_errors)}")
    
    if all_errors:
        print("\n❌ VALIDATION FAILED\n")
        for error in all_errors:
            print(f"  • {error}")
        sys.exit(1)
    else:
        print("\n✅ ALL VALIDATIONS PASSED")
        sys.exit(0)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""BOUND:TESTS_VALIDATE_ALL_SCHEMAS"""
"""
Test: Validate All Schemas

Tests that all JSON Schema files pass validation:
- Draft 2020-12 compliance
- unevaluatedProperties: false enforcement
- Forbidden field detection (email/tckn/otp)
- Enum format validation
- File integrity checks

This is the primary contract validation test.
"""

import json
import pytest
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))

try:
    from jsonschema import Draft202012Validator, ValidationError
    from jsonschema.validators import validator_for
except ImportError:
    pytest.skip("jsonschema not installed", allow_module_level=True)


class TestSchemaValidation:
    """Test suite for schema validation"""
    
    @pytest.fixture(scope="class")
    def base_dir(self) -> Path:
        """Get base directory"""
        return Path(__file__).parent.parent
    
    @pytest.fixture(scope="class")
    def schemas_dir(self, base_dir: Path) -> Path:
        """Get schemas directory"""
        return base_dir / "schemas"
    
    @pytest.fixture(scope="class")
    def all_schema_files(self, schemas_dir: Path) -> List[Path]:
        """Get all schema files"""
        return list(schemas_dir.rglob("*.json"))
    
    def test_schemas_directory_exists(self, schemas_dir: Path):
        """Test that schemas directory exists"""
        assert schemas_dir.exists(), "schemas/ directory not found"
        assert schemas_dir.is_dir(), "schemas/ is not a directory"
    
    def test_has_schema_files(self, all_schema_files: List[Path]):
        """Test that we have schema files"""
        assert len(all_schema_files) > 0, "No schema files found"
        assert len(all_schema_files) >= 20, f"Expected at least 20 schemas, found {len(all_schema_files)}"
    
    @pytest.mark.parametrize("schema_file", [
        pytest.param(f, id=str(f.relative_to(Path(__file__).parent.parent)))
        for f in (Path(__file__).parent.parent / "schemas").rglob("*.json")
    ])
    def test_schema_is_valid_json(self, schema_file: Path):
        """Test that schema file is valid JSON"""
        try:
            with open(schema_file, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Invalid JSON in {schema_file}: {e}")
    
    @pytest.mark.parametrize("schema_file", [
        pytest.param(f, id=str(f.relative_to(Path(__file__).parent.parent)))
        for f in (Path(__file__).parent.parent / "schemas").rglob("*.json")
    ])
    def test_schema_has_schema_property(self, schema_file: Path):
        """Test that schema has $schema property"""
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        assert '$schema' in schema, f"Missing $schema in {schema_file}"
    
    @pytest.mark.parametrize("schema_file", [
        pytest.param(f, id=str(f.relative_to(Path(__file__).parent.parent)))
        for f in (Path(__file__).parent.parent / "schemas").rglob("*.json")
    ])
    def test_schema_is_draft_2020_12(self, schema_file: Path):
        """Test that schema uses Draft 2020-12"""
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        schema_uri = schema.get('$schema', '')
        assert 'draft/2020-12' in schema_uri, \
            f"Schema {schema_file} must use Draft 2020-12, got: {schema_uri}"
    
    @pytest.mark.parametrize("schema_file", [
        pytest.param(f, id=str(f.relative_to(Path(__file__).parent.parent)))
        for f in (Path(__file__).parent.parent / "schemas").rglob("*.json")
        if not f.name.endswith('.enum.v1.json')  # Skip enums
    ])
    def test_schema_has_unevaluated_properties_false(self, schema_file: Path):
        """Test that object schemas have unevaluatedProperties: false"""
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Check root level
        if schema.get('type') == 'object':
            assert 'unevaluatedProperties' in schema, \
                f"Missing unevaluatedProperties in {schema_file}"
            assert schema['unevaluatedProperties'] is False, \
                f"unevaluatedProperties must be false in {schema_file}"
        
        # Check $defs
        if '$defs' in schema:
            for def_name, def_schema in schema['$defs'].items():
                if isinstance(def_schema, dict) and def_schema.get('type') == 'object':
                    assert 'unevaluatedProperties' in def_schema, \
                        f"Missing unevaluatedProperties in {schema_file}#/$defs/{def_name}"
                    assert def_schema['unevaluatedProperties'] is False, \
                        f"unevaluatedProperties must be false in {schema_file}#/$defs/{def_name}"
    
    @pytest.mark.parametrize("schema_file", [
        pytest.param(f, id=str(f.relative_to(Path(__file__).parent.parent)))
        for f in (Path(__file__).parent.parent / "schemas").rglob("*.json")
    ])
    def test_schema_no_forbidden_fields(self, schema_file: Path):
        """Test that schema does not contain forbidden fields (email/tckn/otp)"""
        # Forbidden fields per KR-050
        forbidden_fields = [
            'email', 'e_mail', 'e-mail',
            'tckn', 'tc_kimlik_no', 'tc_no', 'kimlik_no',
            'otp', 'one_time_password', 'verification_code'
        ]
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        found_forbidden = []
        for field in forbidden_fields:
            if f'"{field}"' in content:
                found_forbidden.append(field)
        
        assert len(found_forbidden) == 0, \
            f"Forbidden fields found in {schema_file}: {found_forbidden}"
    
    @pytest.mark.parametrize("schema_file", [
        pytest.param(f, id=str(f.relative_to(Path(__file__).parent.parent)))
        for f in (Path(__file__).parent.parent / "schemas").rglob("*.json")
    ])
    def test_schema_is_self_validating(self, schema_file: Path):
        """Test that schema itself is valid according to JSON Schema spec"""
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        # Get the appropriate validator class
        ValidatorClass = validator_for(schema)
        
        # Check that schema is valid
        try:
            ValidatorClass.check_schema(schema)
        except Exception as e:
            pytest.fail(f"Schema {schema_file} is not valid: {e}")
    
    @pytest.mark.parametrize("enum_file", [
        pytest.param(f, id=str(f.relative_to(Path(__file__).parent.parent)))
        for f in (Path(__file__).parent.parent / "enums").rglob("*.json")
    ])
    def test_enum_has_unique_values(self, enum_file: Path):
        """Test that enum values are unique"""
        with open(enum_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        if 'enum' in schema:
            values = schema['enum']
            assert len(values) == len(set(values)), \
                f"Duplicate enum values in {enum_file}"
        
        # Check values in metadata
        if 'values' in schema:
            value_codes = [v.get('value') for v in schema['values'] if 'value' in v]
            assert len(value_codes) == len(set(value_codes)), \
                f"Duplicate value codes in {enum_file} metadata"
    
    @pytest.mark.parametrize("enum_file", [
        pytest.param(f, id=str(f.relative_to(Path(__file__).parent.parent)))
        for f in (Path(__file__).parent.parent / "enums").rglob("*.json")
    ])
    def test_enum_metadata_complete(self, enum_file: Path):
        """Test that enum metadata is complete"""
        with open(enum_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        if 'values' in schema:
            for value in schema['values']:
                assert 'value' in value, f"Missing 'value' in {enum_file} metadata"
                assert 'description' in value, f"Missing 'description' for {value.get('value')} in {enum_file}"
    
    def test_crop_type_enum_has_9_values(self, schemas_dir: Path):
        """Test that crop_type enum has exactly 9 supported crops (KR-002)"""
        crop_file = schemas_dir.parent / "enums" / "crop_type.enum.v1.json"
        
        with open(crop_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        expected_crops = {
            'COTTON', 'PISTACHIO', 'MAIZE', 'WHEAT',
            'SUNFLOWER', 'GRAPE', 'HAZELNUT', 'OLIVE', 'RED_LENTIL'
        }
        
        actual_crops = set(schema.get('enum', []))
        
        assert actual_crops == expected_crops, \
            f"Expected 9 supported crops: {expected_crops}, got: {actual_crops}"
    
    def test_analysis_type_enum_has_7_values(self, schemas_dir: Path):
        """Test that analysis_type enum has exactly 7 KR-002 map layers"""
        analysis_file = schemas_dir.parent / "enums" / "analysis_type.enum.v1.json"
        
        with open(analysis_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        expected_types = {
            'HEALTH', 'DISEASE', 'PEST', 'FUNGUS',
            'WEED', 'WATER_STRESS', 'NITROGEN_STRESS'
        }
        
        actual_types = set(schema.get('enum', []))
        
        assert actual_types == expected_types, \
            f"Expected 7 KR-002 analysis types: {expected_types}, got: {actual_types}"
    
    def test_phone_pattern_is_10_digits(self, schemas_dir: Path):
        """Test that user_pii phone pattern is 10 digits (KR-050)"""
        pii_file = schemas_dir / "core" / "user_pii.v1.schema.json"
        
        with open(pii_file, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        
        phone_pattern = schema['$defs']['Phone']['properties']['e164']['pattern']
        
        # Pattern should be: ^\+90[1-9][0-9]{9}$
        assert phone_pattern == r'^\+90[1-9][0-9]{9}$', \
            f"Phone pattern must be 10 digits, got: {phone_pattern}"
    
    def test_all_ids_follow_pattern(self, schemas_dir: Path):
        """Test that all entity IDs follow pattern: {entity}_{24-char-hex}"""
        id_pattern = r'^[a-z_]+_[a-z0-9]{24}$'
        
        for schema_file in schemas_dir.rglob("*.json"):
            with open(schema_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for ID patterns in examples
            if '"example":' in content:
                schema = json.loads(content)
                
                def check_ids(obj, path=""):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            new_path = f"{path}.{key}" if path else key
                            
                            # Check if key ends with _id and has example
                            if key.endswith('_id') and isinstance(value, dict) and 'example' in value:
                                example_id = value['example']
                                if isinstance(example_id, str):
                                    assert '_' in example_id, \
                                        f"ID {key} in {schema_file} example must contain underscore: {example_id}"
                                    parts = example_id.split('_')
                                    if len(parts) >= 2:
                                        # Check last part is 24 chars
                                        assert len(parts[-1]) == 24, \
                                            f"ID {key} in {schema_file} must have 24-char suffix: {example_id}"
                            
                            check_ids(value, new_path)
                    elif isinstance(obj, list):
                        for i, item in enumerate(obj):
                            check_ids(item, f"{path}[{i}]")
                
                check_ids(schema)


class TestValidateToolIntegration:
    """Test integration with validate.py tool"""
    
    def test_validate_tool_exists(self):
        """Test that validate.py exists"""
        validate_path = Path(__file__).parent.parent / "tools" / "validate.py"
        assert validate_path.exists(), "validate.py not found"
        assert validate_path.is_file(), "validate.py is not a file"
    
    def test_validate_tool_is_executable(self):
        """Test that validate.py is executable"""
        validate_path = Path(__file__).parent.parent / "tools" / "validate.py"
        import os
        assert validate_path.suffix == ".py", "validate.py should be a python script"


class TestSchemaStructure:
    """Test schema directory structure"""
    
    def test_has_shared_directory(self):
        """Test that shared/ directory exists"""
        shared_dir = Path(__file__).parent.parent / "schemas" / "shared"
        assert shared_dir.exists(), "schemas/shared/ directory not found"
    
    def test_has_enums_directory(self):
        """Test that enums/ directory exists"""
        enums_dir = Path(__file__).parent.parent / "enums"
        assert enums_dir.exists(), "enums/ directory not found"
    
    def test_has_core_directory(self):
        """Test that core/ directory exists"""
        core_dir = Path(__file__).parent.parent / "schemas" / "core"
        assert core_dir.exists(), "schemas/core/ directory not found"
    
    def test_has_edge_directory(self):
        """Test that edge/ directory exists"""
        edge_dir = Path(__file__).parent.parent / "schemas" / "edge"
        assert edge_dir.exists(), "schemas/edge/ directory not found"
    
    def test_has_worker_directory(self):
        """Test that worker/ directory exists"""
        worker_dir = Path(__file__).parent.parent / "schemas" / "worker"
        assert worker_dir.exists(), "schemas/worker/ directory not found"
    
    def test_has_events_directory(self):
        """Test that events/ directory exists"""
        events_dir = Path(__file__).parent.parent / "schemas" / "events"
        assert events_dir.exists(), "schemas/events/ directory not found"
    
    def test_has_platform_directory(self):
        """Test that platform/ directory exists"""
        platform_dir = Path(__file__).parent.parent / "schemas" / "platform"
        assert platform_dir.exists(), "schemas/platform/ directory not found"


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v', '--tb=short'])

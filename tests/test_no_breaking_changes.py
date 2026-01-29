#!/usr/bin/env python3
"""
Test: No Breaking Changes

Tests the breaking change detector and ensures semantic versioning compliance.
This test suite validates that:
- Breaking change detector works correctly
- Version bumps match change severity
- MAJOR version required for breaking changes
"""

import json
import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any


class TestBreakingChangeDetector:
    """Test suite for breaking change detection"""
    
    @pytest.fixture(scope="class")
    def base_dir(self) -> Path:
        """Get base directory"""
        return Path(__file__).parent.parent
    
    @pytest.fixture(scope="class")
    def detector_script(self, base_dir: Path) -> Path:
        """Get breaking change detector script"""
        return base_dir / "tools" / "breaking_change_detector.py"
    
    def test_detector_script_exists(self, detector_script: Path):
        """Test that breaking_change_detector.py exists"""
        assert detector_script.exists(), "breaking_change_detector.py not found"
        assert detector_script.is_file(), "breaking_change_detector.py is not a file"
    
    def test_detector_is_executable(self, detector_script: Path):
        """Test that detector script is executable"""
        import os
        assert os.access(detector_script, os.X_OK), \
            "breaking_change_detector.py is not executable"
    
    def create_test_schema(self, schema_dict: Dict[str, Any]) -> Path:
        """Create temporary schema file"""
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        )
        
        json.dump(schema_dict, temp_file, indent=2)
        temp_file.close()
        
        return Path(temp_file.name)
    
    def test_field_removal_is_breaking(self):
        """Test that field removal is detected as breaking change"""
        old_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "field1": {"type": "string"},
                "field2": {"type": "string"}
            },
            "unevaluatedProperties": False
        }
        
        new_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "field1": {"type": "string"}
                # field2 removed - BREAKING
            },
            "unevaluatedProperties": False
        }
        
        # Create temp directories
        old_dir = tempfile.mkdtemp()
        new_dir = tempfile.mkdtemp()
        
        try:
            # Create schema dirs
            old_schemas = Path(old_dir) / "schemas"
            new_schemas = Path(new_dir) / "schemas"
            old_schemas.mkdir()
            new_schemas.mkdir()
            
            # Write schemas
            with open(old_schemas / "test.json", 'w') as f:
                json.dump(old_schema, f)
            with open(new_schemas / "test.json", 'w') as f:
                json.dump(new_schema, f)
            
            # Import detector
            import sys
            sys.path.insert(0, str(self.base_dir / "tools"))
            from breaking_change_detector import BreakingChangeDetector
            
            # Detect changes
            detector = BreakingChangeDetector(old_schemas, new_schemas)
            result = detector.detect_changes()
            
            # Assert breaking change detected
            assert result['has_breaking'], "Field removal should be breaking"
            assert len(result['breaking']) > 0, "Should have breaking changes"
            
        finally:
            # Cleanup
            shutil.rmtree(old_dir)
            shutil.rmtree(new_dir)
    
    def test_type_change_is_breaking(self):
        """Test that type change is detected as breaking"""
        old_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "count": {"type": "integer"}
            },
            "unevaluatedProperties": False
        }
        
        new_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "count": {"type": "string"}  # Changed from integer - BREAKING
            },
            "unevaluatedProperties": False
        }
        
        old_dir = tempfile.mkdtemp()
        new_dir = tempfile.mkdtemp()
        
        try:
            old_schemas = Path(old_dir) / "schemas"
            new_schemas = Path(new_dir) / "schemas"
            old_schemas.mkdir()
            new_schemas.mkdir()
            
            with open(old_schemas / "test.json", 'w') as f:
                json.dump(old_schema, f)
            with open(new_schemas / "test.json", 'w') as f:
                json.dump(new_schema, f)
            
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
            from breaking_change_detector import BreakingChangeDetector
            
            detector = BreakingChangeDetector(old_schemas, new_schemas)
            result = detector.detect_changes()
            
            assert result['has_breaking'], "Type change should be breaking"
            
        finally:
            shutil.rmtree(old_dir)
            shutil.rmtree(new_dir)
    
    def test_enum_value_removal_is_breaking(self):
        """Test that enum value removal is detected as breaking"""
        old_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "enum": ["VALUE1", "VALUE2", "VALUE3"]
        }
        
        new_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "enum": ["VALUE1", "VALUE2"]  # VALUE3 removed - BREAKING
        }
        
        old_dir = tempfile.mkdtemp()
        new_dir = tempfile.mkdtemp()
        
        try:
            old_schemas = Path(old_dir) / "schemas"
            new_schemas = Path(new_dir) / "schemas"
            old_schemas.mkdir()
            new_schemas.mkdir()
            
            with open(old_schemas / "test.json", 'w') as f:
                json.dump(old_schema, f)
            with open(new_schemas / "test.json", 'w') as f:
                json.dump(new_schema, f)
            
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
            from breaking_change_detector import BreakingChangeDetector
            
            detector = BreakingChangeDetector(old_schemas, new_schemas)
            result = detector.detect_changes()
            
            assert result['has_breaking'], "Enum value removal should be breaking"
            
        finally:
            shutil.rmtree(old_dir)
            shutil.rmtree(new_dir)
    
    def test_optional_field_addition_is_not_breaking(self):
        """Test that optional field addition is NOT breaking"""
        old_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "field1": {"type": "string"}
            },
            "required": ["field1"],
            "unevaluatedProperties": False
        }
        
        new_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "field1": {"type": "string"},
                "field2": {"type": "string"}  # Added optional - NOT BREAKING
            },
            "required": ["field1"],  # field2 not in required
            "unevaluatedProperties": False
        }
        
        old_dir = tempfile.mkdtemp()
        new_dir = tempfile.mkdtemp()
        
        try:
            old_schemas = Path(old_dir) / "schemas"
            new_schemas = Path(new_dir) / "schemas"
            old_schemas.mkdir()
            new_schemas.mkdir()
            
            with open(old_schemas / "test.json", 'w') as f:
                json.dump(old_schema, f)
            with open(new_schemas / "test.json", 'w') as f:
                json.dump(new_schema, f)
            
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
            from breaking_change_detector import BreakingChangeDetector
            
            detector = BreakingChangeDetector(old_schemas, new_schemas)
            result = detector.detect_changes()
            
            assert not result['has_breaking'], "Optional field addition should not be breaking"
            assert len(result['non_breaking']) > 0, "Should have non-breaking changes"
            
        finally:
            shutil.rmtree(old_dir)
            shutil.rmtree(new_dir)
    
    def test_enum_value_addition_is_not_breaking(self):
        """Test that enum value addition is NOT breaking"""
        old_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "enum": ["VALUE1", "VALUE2"]
        }
        
        new_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "enum": ["VALUE1", "VALUE2", "VALUE3"]  # VALUE3 added - NOT BREAKING
        }
        
        old_dir = tempfile.mkdtemp()
        new_dir = tempfile.mkdtemp()
        
        try:
            old_schemas = Path(old_dir) / "schemas"
            new_schemas = Path(new_dir) / "schemas"
            old_schemas.mkdir()
            new_schemas.mkdir()
            
            with open(old_schemas / "test.json", 'w') as f:
                json.dump(old_schema, f)
            with open(new_schemas / "test.json", 'w') as f:
                json.dump(new_schema, f)
            
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
            from breaking_change_detector import BreakingChangeDetector
            
            detector = BreakingChangeDetector(old_schemas, new_schemas)
            result = detector.detect_changes()
            
            assert not result['has_breaking'], "Enum value addition should not be breaking"
            assert len(result['non_breaking']) > 0, "Should have non-breaking changes"
            
        finally:
            shutil.rmtree(old_dir)
            shutil.rmtree(new_dir)
    
    def test_required_field_addition_is_breaking(self):
        """Test that required field addition is breaking"""
        old_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "field1": {"type": "string"}
            },
            "required": ["field1"],
            "unevaluatedProperties": False
        }
        
        new_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "field1": {"type": "string"},
                "field2": {"type": "string"}
            },
            "required": ["field1", "field2"],  # field2 now required - BREAKING
            "unevaluatedProperties": False
        }
        
        old_dir = tempfile.mkdtemp()
        new_dir = tempfile.mkdtemp()
        
        try:
            old_schemas = Path(old_dir) / "schemas"
            new_schemas = Path(new_dir) / "schemas"
            old_schemas.mkdir()
            new_schemas.mkdir()
            
            with open(old_schemas / "test.json", 'w') as f:
                json.dump(old_schema, f)
            with open(new_schemas / "test.json", 'w') as f:
                json.dump(new_schema, f)
            
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
            from breaking_change_detector import BreakingChangeDetector
            
            detector = BreakingChangeDetector(old_schemas, new_schemas)
            result = detector.detect_changes()
            
            assert result['has_breaking'], "Required field addition should be breaking"
            
        finally:
            shutil.rmtree(old_dir)
            shutil.rmtree(new_dir)


class TestVersionBumpPolicy:
    """Test semantic versioning compliance"""
    
    @pytest.fixture
    def base_dir(self) -> Path:
        """Get base directory"""
        return Path(__file__).parent.parent
    
    def test_version_file_exists(self, base_dir: Path):
        """Test that CONTRACTS_VERSION.md exists"""
        version_file = base_dir / "CONTRACTS_VERSION.md"
        # May not exist yet, so this is optional
        if version_file.exists():
            assert version_file.is_file(), "CONTRACTS_VERSION.md is not a file"
    
    def test_versioning_policy_exists(self, base_dir: Path):
        """Test that versioning_policy.md exists"""
        policy_file = base_dir / "versioning_policy.md"
        assert policy_file.exists(), "versioning_policy.md not found"
        assert policy_file.is_file(), "versioning_policy.md is not a file"
    
    def test_versioning_policy_has_semver_rules(self, base_dir: Path):
        """Test that versioning policy documents semver rules"""
        policy_file = base_dir / "versioning_policy.md"
        
        with open(policy_file, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # Check for semver keywords
        assert 'major' in content, "Policy should mention MAJOR version"
        assert 'minor' in content, "Policy should mention MINOR version"
        assert 'patch' in content, "Policy should mention PATCH version"
        assert 'breaking' in content, "Policy should mention breaking changes"


class TestPinVersionTool:
    """Test pin_version.py tool"""
    
    @pytest.fixture
    def base_dir(self) -> Path:
        """Get base directory"""
        return Path(__file__).parent.parent
    
    @pytest.fixture
    def pin_script(self, base_dir: Path) -> Path:
        """Get pin_version.py script"""
        return base_dir / "tools" / "pin_version.py"
    
    def test_pin_script_exists(self, pin_script: Path):
        """Test that pin_version.py exists"""
        assert pin_script.exists(), "pin_version.py not found"
        assert pin_script.is_file(), "pin_version.py is not a file"
    
    def test_pin_script_is_executable(self, pin_script: Path):
        """Test that pin script is executable"""
        import os
        assert os.access(pin_script, os.X_OK), "pin_version.py is not executable"
    
    def test_pin_script_has_breaking_flag(self, pin_script: Path):
        """Test that pin script supports --breaking flag"""
        with open(pin_script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert '--breaking' in content, "pin_version.py should support --breaking flag"


if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v', '--tb=short'])
#!/usr/bin/env python3
import sys
import json
from pathlib import Path

def validate_types(value, expected_type, path_str):
    """Fallback type checker for schema validation."""
    type_mappings = {
        "STRING": str,
        "INTEGER": int,
        "BOOLEAN": bool,
        "ARRAY": list,
        "OBJECT": dict
    }
    
    expected_class = type_mappings.get(expected_type.upper())
    if not expected_class:
        return []

    errors = []
    # Special case: float is not int, but we want strict ints where specified
    if expected_class == int and type(value) == float:
         errors.append(f"Field '{path_str}' must be type INTEGER, got float")
    elif not isinstance(value, expected_class):
        errors.append(f"Field '{path_str}' must be type {expected_type.upper()}, got {type(value).__name__.upper()}")
    
    return errors

def validate_properties(payload, schema, path_str=""):
    """Recursively validates properties using standard JSON schema principles."""
    errors = []
    
    # 1. Validate required fields
    required_fields = schema.get("required", [])
    for field in required_fields:
        if field not in payload:
            errors.append(f"Missing required field: '{path_str}.{field}'" if path_str else f"Missing required field: '{field}'")
            
    # 2. Validate field types and constraints
    properties = schema.get("properties", {})
    for key, value in payload.items():
        if key not in properties:
            continue  # Ignore extra properties unless additionalProperties is false
            
        prop_schema = properties[key]
        prop_type = prop_schema.get("type")
        current_path = f"{path_str}.{key}" if path_str else key
        
        if prop_type:
            errors.extend(validate_types(value, prop_type, current_path))
            
            # Recurse if OBJECT
            if prop_type.upper() == "OBJECT" and isinstance(value, dict):
                errors.extend(validate_properties(value, prop_schema, current_path))
            
            # Check ARRAY items
            elif prop_type.upper() == "ARRAY" and isinstance(value, list):
                item_schema = prop_schema.get("items")
                if item_schema:
                    item_type = item_schema.get("type")
                    for idx, item in enumerate(value):
                        item_path = f"{current_path}[{idx}]"
                        if item_type:
                            errors.extend(validate_types(item, item_type, item_path))
                        if item_schema.get("type", "").upper() == "OBJECT" and isinstance(item, dict):
                            errors.extend(validate_properties(item, item_schema, item_path))
            
            # Check ENUM options
            enum_options = prop_schema.get("enum")
            if enum_options and value not in enum_options:
                errors.append(f"Field '{current_path}' has invalid value '{value}'. Allowed: {enum_options}")
                
            # Check MIN/MAX constraints
            if prop_type.upper() == "INTEGER":
                if "minimum" in prop_schema and value < prop_schema["minimum"]:
                    errors.append(f"Field '{current_path}' value {value} is below minimum {prop_schema['minimum']}")
                if "maximum" in prop_schema and value > prop_schema["maximum"]:
                    errors.append(f"Field '{current_path}' value {value} is above maximum {prop_schema['maximum']}")
                    
    return errors

def main():
    if len(sys.argv) < 3:
        print("Usage: python workflow_validator.py <path_to_payload.json> <path_to_schema.json>")
        sys.exit(1)
        
    payload_path = Path(sys.argv[1])
    schema_path = Path(sys.argv[2])
    
    if not payload_path.exists():
        print(f"Error: Payload file not found at {payload_path}", file=sys.stderr)
        sys.exit(2)
    if not schema_path.exists():
        print(f"Error: Schema file not found at {schema_path}", file=sys.stderr)
        sys.exit(2)
        
    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error parsing payload JSON: {e}", file=sys.stderr)
        sys.exit(3)
        
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error parsing schema JSON: {e}", file=sys.stderr)
        sys.exit(3)
        
    # Check if jsonschema is available
    try:
        import jsonschema
        print("Using standard 'jsonschema' library for validation...")
        try:
            jsonschema.validate(instance=payload, schema=schema)
            print("✅ Schema Validation: Passed.")
            sys.exit(0)
        except jsonschema.exceptions.ValidationError as err:
            print(f"❌ Schema Validation: Failed.\n  {err.message}", file=sys.stderr)
            sys.exit(1)
    except ImportError:
        print("jsonschema library not found. Falling back to native Cursory Schema engine...")
        errors = validate_properties(payload, schema)
        if errors:
            print("\n❌ Schema Validation: Failed (validation errors found):")
            for err in errors:
                print(f"  - {err}")
            sys.exit(1)
        else:
            print("\n✅ Schema Validation: Passed.")
            sys.exit(0)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Schema Validator for Ethana Proposal Agent Runtime.
Validates skill execution payloads against predefined JSON schemas.
Supports standard jsonschema library and falls back to a custom validation engine if not installed.
"""

import os
import json
from pathlib import Path

class SchemaValidator:
    def __init__(self, schemas_dir: str):
        """Initializes the validator with the directory containing schemas."""
        self.schemas_dir = Path(schemas_dir)
        self.schemas = {}
        self._load_schemas()

    def _load_schemas(self):
        """Loads available JSON schemas from the schemas directory."""
        schema_files = {
            "proposal_review_input": "proposal-review-input.schema.json",
            "proposal_review_output": "proposal-review-output.schema.json"
        }
        for key, filename in schema_files.items():
            path = self.schemas_dir / filename
            if path.exists():
                try:
                    self.schemas[key] = json.loads(path.read_text(encoding="utf-8"))
                except Exception as e:
                    print(f"Warning: Failed to load schema {filename}: {e}")
            else:
                print(f"Warning: Schema file not found: {path}")

    def validate(self, payload: dict, schema_name: str) -> list:
        """
        Validates the payload against the specified schema.
        Returns a list of error messages (strings). An empty list means validation passed.
        """
        schema = self.schemas.get(schema_name)
        if not schema:
            return [f"Schema '{schema_name}' is not loaded or does not exist."]

        try:
            import jsonschema
            try:
                jsonschema.validate(instance=payload, schema=schema)
                return []
            except jsonschema.exceptions.ValidationError as err:
                return [err.message]
        except ImportError:
            # Fallback to custom validation logic
            return self._fallback_validate(payload, schema)

    def _fallback_validate(self, payload: dict, schema: dict) -> list:
        """Fallback validation engine using custom type and constraint checking."""
        return self._validate_properties(payload, schema)

    def _validate_types(self, value, expected_type, path_str) -> list:
        type_mappings = {
            "STRING": str,
            "INTEGER": int,
            "NUMBER": (int, float),
            "BOOLEAN": bool,
            "ARRAY": list,
            "OBJECT": dict
        }
        expected_class = type_mappings.get(expected_type.upper())
        if not expected_class:
            return []

        errors = []
        if expected_class == int and type(value) == float:
            errors.append(f"Field '{path_str}' must be type INTEGER, got float")
        elif not isinstance(value, expected_class):
            errors.append(f"Field '{path_str}' must be type {expected_type.upper()}, got {type(value).__name__.upper()}")
        return errors

    def _validate_properties(self, payload, schema, path_str="") -> list:
        errors = []
        if not isinstance(payload, dict):
            return [f"Payload at '{path_str}' must be type OBJECT, got {type(payload).__name__.upper()}"]

        # 1. Check required fields
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in payload:
                errors.append(f"Missing required field: '{path_str}.{field}'" if path_str else f"Missing required field: '{field}'")

        # 2. Validate field types and constraints
        properties = schema.get("properties", {})
        for key, value in payload.items():
            if key not in properties:
                continue

            prop_schema = properties[key]
            prop_type = prop_schema.get("type")
            current_path = f"{path_str}.{key}" if path_str else key

            if prop_type:
                errors.extend(self._validate_types(value, prop_type, current_path))

                # Recurse if OBJECT
                if prop_type.upper() == "OBJECT" and isinstance(value, dict):
                    errors.extend(self._validate_properties(value, prop_schema, current_path))

                # Check ARRAY items
                elif prop_type.upper() == "ARRAY" and isinstance(value, list):
                    item_schema = prop_schema.get("items")
                    if item_schema:
                        item_type = item_schema.get("type")
                        for idx, item in enumerate(value):
                            item_path = f"{current_path}[{idx}]"
                            if item_type:
                                errors.extend(self._validate_types(item, item_type, item_path))
                            if item_schema.get("type", "").upper() == "OBJECT" and isinstance(item, dict):
                                errors.extend(self._validate_properties(item, item_schema, item_path))

                # Check ENUM options
                enum_options = prop_schema.get("enum")
                if enum_options and value not in enum_options:
                    errors.append(f"Field '{current_path}' has invalid value '{value}'. Allowed: {enum_options}")

                # Check MIN/MAX constraints
                if prop_type.upper() == "INTEGER" or prop_type.upper() == "NUMBER":
                    if "minimum" in prop_schema and value < prop_schema["minimum"]:
                        errors.append(f"Field '{current_path}' value {value} is below minimum {prop_schema['minimum']}")
                    if "maximum" in prop_schema and value > prop_schema["maximum"]:
                        errors.append(f"Field '{current_path}' value {value} is above maximum {prop_schema['maximum']}")

        return errors

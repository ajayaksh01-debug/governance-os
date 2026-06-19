#!/usr/bin/env python3
import json
from pathlib import Path


class SchemaValidator:
    def __init__(self, schemas_dir: str):
        self.schemas_dir = Path(schemas_dir)
        self.schemas = {}
        self._load_schemas()

    def _load_schemas(self):
        schema_files = {
            "regulatory_mapping_output": "regulatory_mapping_output.json",
            "control_mapping_output": "control_mapping_output.json",
            "solution_mapping_output": "solution_mapping_output.json",
            "iso42001_output": "iso-42001-gap-assessment-output.schema.json",
            "capability_validation_output": "ethana-capability-validation-output.schema.json",
            "proposal_review_output": "proposal-review-output.schema.json",
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
            return self._fallback_validate(payload, schema)

    def _fallback_validate(self, payload: dict, schema: dict) -> list:
        return self._validate_object(payload, schema, "")

    def _validate_object(self, payload, schema: dict, path: str) -> list:
        errors = []
        if not isinstance(payload, dict):
            return [f"Expected object at '{path}', got {type(payload).__name__}"]

        for field in schema.get("required", []):
            if field not in payload:
                loc = f"{path}.{field}" if path else field
                errors.append(f"Missing required field: '{loc}'")

        for key, value in payload.items():
            prop_schema = schema.get("properties", {}).get(key)
            if not prop_schema:
                continue
            loc = f"{path}.{key}" if path else key
            prop_type = prop_schema.get("type", "")
            errors.extend(self._check_type(value, prop_type, loc))
            if prop_type == "object" and isinstance(value, dict):
                errors.extend(self._validate_object(value, prop_schema, loc))
            elif prop_type == "array" and isinstance(value, list):
                item_schema = prop_schema.get("items", {})
                for i, item in enumerate(value):
                    item_loc = f"{loc}[{i}]"
                    item_type = item_schema.get("type", "")
                    errors.extend(self._check_type(item, item_type, item_loc))
                    if item_type == "object" and isinstance(item, dict):
                        errors.extend(self._validate_object(item, item_schema, item_loc))
            enum_vals = prop_schema.get("enum")
            if enum_vals is not None and value not in enum_vals:
                errors.append(
                    f"Field '{loc}' value '{value}' not in enum {enum_vals}"
                )

        return errors

    def _check_type(self, value, expected_type: str, path: str) -> list:
        type_map = {
            "string": str,
            "integer": int,
            "number": (int, float),
            "boolean": bool,
            "array": list,
            "object": dict,
        }
        if not expected_type:
            return []
        expected_class = type_map.get(expected_type.lower())
        if expected_class is None:
            return []
        if expected_type.lower() == "integer" and isinstance(value, bool):
            return [f"Field '{path}' must be integer, got bool"]
        if not isinstance(value, expected_class):
            return [
                f"Field '{path}' must be {expected_type}, got {type(value).__name__}"
            ]
        return []

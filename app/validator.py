# app/validator.py
from typing import Dict, Any, List, Tuple
import json, os
from jsonschema import Draft202012Validator

def load_schema(path: str = None) -> Dict[str, Any]:
    if path is None:
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schema", "postschema.v1.schema.json")
    with open(path, "r") as f:
        return json.load(f)

def validate_payload(payload: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[Dict[str, Any]], List[str]]:
    validator = Draft202012Validator(schema)
    errors_list = []
    for e in sorted(validator.iter_errors(payload), key=lambda x: x.path):
        errors_list.append({
            "path": "/"+"/".join([str(p) for p in e.path]),
            "code": e.validator,
            "message": e.message,
            "provenance": payload.get("provenance", [])
        })
    return (len(errors_list) == 0, errors_list, payload.get("_warnings", []))

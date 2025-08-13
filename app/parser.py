# app/parser.py
# Deterministic converter. Replace TODO sections with real parsing/grammars for .PST and .pas.
from typing import Dict, Any, List
import re

def _extract_exep_calls(pst_text: str) -> List[str]:
    exeps = re.findall(r"EXEP\s*\(.*?,\s*([A-Za-z0-9_]+)\s*\)", pst_text)
    return list(dict.fromkeys(exeps))

def _symbol_table_pas(pas_text: str) -> List[str]:
    procs = re.findall(r"(?i)\bprocedure\s+([A-Za-z0-9_]+)", pas_text)
    return list(dict.fromkeys(procs))

def convert_pst_pas(pst_text: str, pas_text: str) -> Dict[str, Any]:
    exeps = _extract_exep_calls(pst_text)
    symbols = _symbol_table_pas(pas_text)
    missing = [h for h in exeps if h not in symbols]

    payload: Dict[str, Any] = {
        "machine": {"make": "TRUMPF", "model": "TC5000R", "controller": "Unknown"},
        "machine_settings": {"_note": "TODO: parse from PST numeric families"},
        "process_mappings": [],
        "canned_cycles": [],
        "provenance": []
    }

    for h in exeps:
        payload["provenance"].append({"pst_section": "Start of File", "line": 0, "raw": f"EXEP(...,{h})", "handler": h})

    if missing:
        payload["_warnings"] = {"orphan_handlers": missing}

    return payload

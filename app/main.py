from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Any, Dict
from app.validator import load_schema, validate_payload
from app.parser import convert_pst_pas

app = FastAPI(title="SigmaNEST Post Converter", version="1.0")  # ✅

# Serve the web UI
app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/healthz")  # ✅
def healthz():
    return {"ok": True, "version": "1.0"}

@app.post("/convert")
async def convert(pst: UploadFile = File(...), pas: UploadFile = File(...)) -> Dict[str, Any]:
    if not pst or not pas:
        raise HTTPException(status_code=400, detail="Both pst and pas files are required.")
    pst_bytes = await pst.read()
    pas_bytes = await pas.read()
    try:
        result = convert_pst_pas(pst_bytes.decode(errors="ignore"), pas_bytes.decode(errors="ignore"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parse/convert error: {e}")
    return result

@app.post("/validate")
async def validate_endpoint(payload: Dict[str, Any]) -> Dict[str, Any]:
    schema = load_schema()
    valid, errors, warnings = validate_payload(payload, schema)
    return {"valid": valid, "errors": errors, "warnings": warnings}

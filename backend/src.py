from fastapi import FastAPI
import sys
from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
from backend.event_register import eventbrite_adapter

app = FastAPI()
@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/v1/payment_context")
def payment_context(payload:eventbrite_adapter.PaymentContextPayload):
    print("Received payment context:", payload.model_dump())
    return {
        "status": "context received",
        "status_code": 200
        }
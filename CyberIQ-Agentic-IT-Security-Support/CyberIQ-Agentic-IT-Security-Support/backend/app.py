import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import settings
from .rcs import send_rcs_text
from .router import route
from agents.network_agent import handle as network_handle
from agents.security_agent import handle as security_handle

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
logger = logging.getLogger("cyberiq")

app = FastAPI(title="CyberIQ", version="0.1.0", description="Agentic IT & Security Support")


class SupportRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    destination_phone_number: Optional[str] = None
    send_response: bool = False


class InboundRcsRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    destination_phone_number: Optional[str] = None


def process_message(message: str) -> dict:
    routing = route(message)
    responses = []
    for intent in routing["intents"]:
        if intent == "network":
            responses.append(network_handle(message))
        elif intent == "security":
            responses.append(security_handle(message))
        else:
            responses.append("General Agent: Please provide a little more detail so I can route this request.")

    combined = "\n\n".join(responses)
    escalation = routing["priority"] == "high" or "security" in routing["intents"]
    if escalation:
        combined += "\n\nCyberIQ: This request is marked for SOC/security review because it may involve a security incident."

    return {
        "routing": routing,
        "response": combined,
        "escalation_recommended": escalation,
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "CyberIQ"}


@app.post("/support")
def support(req: SupportRequest):
    result = process_message(req.message)
    if req.send_response:
        if not req.destination_phone_number:
            raise HTTPException(status_code=400, detail="destination_phone_number is required when send_response=true")
        try:
            result["rcs"] = send_rcs_text(req.destination_phone_number, result["response"])
        except Exception as exc:
            logger.exception("RCS send failed")
            raise HTTPException(status_code=502, detail=f"RCS send failed: {exc}") from exc
    return result


@app.post("/webhook/rcs")
def inbound_rcs(req: InboundRcsRequest):
    """Application-level webhook shape for an inbound RCS/SNS adapter.

    AWS End User Messaging publishes inbound RCS messages to SNS. In production,
    an SNS subscription/Lambda should validate the SNS envelope and call this
    endpoint with the normalized message and destination number.
    """
    result = process_message(req.message)
    if req.destination_phone_number:
        try:
            result["rcs"] = send_rcs_text(req.destination_phone_number, result["response"])
        except Exception as exc:
            logger.exception("RCS reply failed")
            result["rcs_error"] = str(exc)
    return result

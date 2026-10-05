import json
import logging
from typing import Any

import boto3

from .config import settings

logger = logging.getLogger(__name__)


def _client():
    return boto3.client("bedrock-runtime", region_name=settings.aws_region)


def converse(system_prompt: str, user_prompt: str) -> str:
    """Call Amazon Bedrock Converse when configured.

    The model ID is intentionally supplied by environment variable because
    model availability and access vary by AWS account and region.
    """
    if not settings.use_bedrock or not settings.bedrock_model_id:
        raise RuntimeError("Bedrock is not configured (set USE_BEDROCK=true and BEDROCK_MODEL_ID).")

    response = _client().converse(
        modelId=settings.bedrock_model_id,
        system=[{"text": system_prompt}],
        messages=[{"role": "user", "content": [{"text": user_prompt}]}],
        inferenceConfig={"temperature": 0.1, "maxTokens": 600},
    )
    parts = response.get("output", {}).get("message", {}).get("content", [])
    text_parts = [p.get("text", "") for p in parts if "text" in p]
    return "".join(text_parts).strip()


def classify(message: str) -> dict[str, Any]:
    system = (
        "You are CyberIQ's intent router. Return ONLY valid JSON with keys "
        "intents (array containing zero or more of network, security, general), "
        "priority (low, medium, high), and reason (short string). "
        "Choose security for suspicious login, malware, phishing, credential, "
        "or security-alert issues; network for VPN, DNS, Wi-Fi, routing, "
        "connectivity, firewall, or access issues."
    )
    raw = converse(system, message)
    return json.loads(raw)

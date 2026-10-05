import json
import logging
import re

from .bedrock import classify

logger = logging.getLogger(__name__)

NETWORK_TERMS = re.compile(r"\b(vpn|network|dns|wifi|wi-fi|internet|router|routing|firewall|connect|connection|latency|packet)\b", re.I)
SECURITY_TERMS = re.compile(r"\b(suspicious|phishing|malware|ransomware|credential|password|login alert|breach|security alert|unauthori[sz]ed|attack|threat|virus)\b", re.I)


def heuristic_route(message: str) -> dict:
    intents = []
    if NETWORK_TERMS.search(message):
        intents.append("network")
    if SECURITY_TERMS.search(message):
        intents.append("security")
    if not intents:
        intents = ["general"]
    priority = "high" if "security" in intents else "medium" if "network" in intents else "low"
    return {"intents": intents, "priority": priority, "reason": "Keyword-based fallback router"}


def route(message: str) -> dict:
    try:
        result = classify(message)
        intents = [i for i in result.get("intents", []) if i in {"network", "security", "general"}]
        if not intents:
            raise ValueError("No valid intent returned")
        return {
            "intents": intents,
            "priority": result.get("priority", "medium"),
            "reason": result.get("reason", "Bedrock intent classification"),
            "engine": "amazon-bedrock",
        }
    except Exception as exc:
        logger.warning("Bedrock routing unavailable: %s", exc)
        result = heuristic_route(message)
        result["engine"] = "heuristic-fallback"
        return result

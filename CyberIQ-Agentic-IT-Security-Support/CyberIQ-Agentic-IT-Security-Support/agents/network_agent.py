from backend.bedrock import converse
from backend.config import settings


def handle(message: str) -> str:
    if settings.use_bedrock and settings.bedrock_model_id:
        try:
            return converse(
                "You are CyberIQ Network Agent. Provide safe IT network troubleshooting. "
                "Do not invent telemetry. Ask for the minimum missing detail. "
                "For VPN issues, suggest checks such as credentials/MFA, client status, "
                "DNS, route, and gateway reachability. Escalate when access or outage risk is high.",
                message,
            )
        except Exception:
            pass
    return (
        "Network Agent: I can help troubleshoot this. Please check VPN client status, "
        "credentials/MFA, DNS resolution, and reachability to the VPN gateway. "
        "If those checks fail or multiple users are affected, escalate to the network team."
    )

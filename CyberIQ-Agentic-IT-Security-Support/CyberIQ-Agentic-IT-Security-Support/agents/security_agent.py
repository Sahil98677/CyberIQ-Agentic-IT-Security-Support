from backend.bedrock import converse
from backend.config import settings


def handle(message: str) -> str:
    if settings.use_bedrock and settings.bedrock_model_id:
        try:
            return converse(
                "You are CyberIQ Security Agent. Respond as a defensive SOC/security support analyst. "
                "Never claim an incident is confirmed without evidence. For suspicious-login alerts, "
                "recommend verifying the sign-in source, revoking sessions if policy permits, resetting "
                "credentials through approved processes, checking MFA, and escalating high-risk activity. "
                "Do not request secrets, passwords, or MFA codes.",
                message,
            )
        except Exception:
            pass
    return (
        "Security Agent: Treat the suspicious login as potentially high risk. Do not share passwords or "
        "MFA codes. Verify the alert details, review the sign-in source, secure the account using your "
        "approved process, and escalate to the SOC if the activity is not recognized."
    )

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    aws_region: str = os.getenv("AWS_REGION", "ap-south-1")
    rcs_origination_identity: str = os.getenv("RCS_ORIGINATION_IDENTITY", "")
    rcs_message_type: str = os.getenv("RCS_MESSAGE_TYPE", "TRANSACTIONAL")
    bedrock_model_id: str = os.getenv("BEDROCK_MODEL_ID", "")
    use_bedrock: bool = os.getenv("USE_BEDROCK", "true").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()

import logging

import boto3

from .config import settings

logger = logging.getLogger(__name__)


def send_rcs_text(destination_phone_number: str, body: str) -> dict:
    """Send text through AWS End User Messaging.

    AWS uses the Pinpoint SMS and Voice v2 API. When the origination identity
    is an AWS RCS Agent ARN, SendTextMessage routes the text over RCS.
    A pool can also be used when SMS fallback is desired.
    """
    if not settings.rcs_origination_identity:
        raise RuntimeError("RCS_ORIGINATION_IDENTITY is not configured.")

    client = boto3.client("pinpoint-sms-voice-v2", region_name=settings.aws_region)
    return client.send_text_message(
        DestinationPhoneNumber=destination_phone_number,
        OriginationIdentity=settings.rcs_origination_identity,
        MessageBody=body,
        MessageType=settings.rcs_message_type,
    )

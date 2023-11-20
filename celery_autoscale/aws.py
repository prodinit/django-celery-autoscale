import boto3
import botocore
from botocore.config import Config
from .exceptions import UnknownAWSServiceException
from typing import Optional

BOTO3_CONFIG = Config(retries=dict(max_attempts=10), signature_version="s3v4")


def get_boto_client(
    service_name: str,
    AWS_REGION_NAME: Optional[str] = None,
    AWS_ACCESS_KEY_ID: Optional[str] = None,
    AWS_SECRET_ACCESS_KEY: Optional[str] = None,
    AWS_SESSION_TOKEN: Optional[str] = None,
) -> boto3.client or None:
    """
    Returns boto3 client for the provided service name
    """
    try:
        if service_name:
            client = boto3.client(
                service_name,
                region_name=AWS_REGION_NAME,
                config=BOTO3_CONFIG,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                aws_session_token=AWS_SESSION_TOKEN,
            )

            return client
        return None
    except botocore.exceptions.UnknownServiceError:
        raise UnknownAWSServiceException(f"Unknown AWS Service Error: {service_name}")

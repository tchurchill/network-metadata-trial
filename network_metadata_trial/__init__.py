import random
import logging
import json
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

logger = logging.getLogger(__name__)


def get_random_secret_key():
    return "".join(
        random.SystemRandom().choice(
            "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        )
        for i in range(50)
    )


def get_asm_secret(key: str, secret_arn: str) -> str:
    client = boto3.client("secretsmanager", region_name="us-east-1")
    try:
        secret_value_rsp = client.get_secret_value(SecretId=secret_arn)
    except ClientError as e:
        logger.error(e)
        logger.error(e.response.get("Error", {}).get("Code", ""))
        logger.error(e.response.get("Error", {}).get("Message", ""))
        raise Exception("Exception retrieving django secret")
    secure_string = secret_value_rsp["SecretString"]
    return json.loads(secure_string).get(key, "")

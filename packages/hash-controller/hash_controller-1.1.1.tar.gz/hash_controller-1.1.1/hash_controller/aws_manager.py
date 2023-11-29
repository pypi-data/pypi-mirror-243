import boto3
from botocore.exceptions import ClientError

from hash_controller.settings import Settings

settings = Settings()


def get_secret(key: str):
    # Create a Secrets Manager client
    client = boto3.client(
        "secretsmanager",
        aws_access_key_id=settings.AWS_CREDENTIAL_KEY,
        aws_secret_access_key=settings.AWS_CREDENTIAL_SECRET,
        region_name=settings.AWS_REGION,
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=key)
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    return get_secret_value_response["SecretString"]

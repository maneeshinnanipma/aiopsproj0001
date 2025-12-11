
import boto3
from typing import Optional

def get_bedrock_client(aws_access_key_id: Optional[str]=None,
                       aws_secret_access_key: Optional[str]=None,
                       region_name: str="us-east-1"):
    # Prefer provider chain / SSO / role
    if aws_access_key_id and aws_secret_access_key:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )
    else:
        session = boto3.Session(region_name=region_name)
    return session.client("bedrock-runtime")

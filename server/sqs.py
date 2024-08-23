import os
from aioboto3 import Session

host = "127.0.0.1" if os.getenv("LOCAL") else "localstack"


def get_sqs():
    session = Session()
    return session.resource(
        "sqs",
        endpoint_url=f"http://{host}:4566",
        region_name="eu-north-1",
        aws_access_key_id="mock",
        aws_secret_access_key="mock",
        aws_session_token="mock",
    )

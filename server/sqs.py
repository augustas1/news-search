from aioboto3 import Session


def get_sqs():
    session = Session()
    return session.resource("sqs", endpoint_url="http://127.0.0.1:4566")

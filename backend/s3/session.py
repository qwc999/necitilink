import aioboto3
from functools import wraps
from config.settings import (
    MINIO_URL,
    MINIO_ROOT_PASSWORD,
    MINIO_ROOT_USER
)


def aioboto_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=MINIO_URL,
            aws_access_key_id=MINIO_ROOT_USER,
            aws_secret_access_key=MINIO_ROOT_PASSWORD,
        ) as s3_client:
            return await func(*args, s3_client=s3_client, **kwargs)
    return wrapper

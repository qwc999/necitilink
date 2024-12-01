from io import BytesIO
from .session import aioboto_session


@aioboto_session
async def create_bucket(s3_client, bucket_name: str = "bucket"):
    await s3_client.create_bucket(Bucket=bucket_name)

  
@aioboto_session
async def upload_file(
    filename: str,
    file_bytes: BytesIO, 
    s3_client, 
    bucket_name: str = "bucket"):
    await s3_client.put_object(
        Bucket=bucket_name, 
        Key=filename, 
        Body=file_bytes
    )

@aioboto_session
async def download_file(filename: str, s3_client, bucket_name: str = "bucket") -> BytesIO:
    file_stream = BytesIO()
    await s3_client.download_fileobj(
        bucket_name, 
        filename, 
        file_stream
    )
    file_stream.seek(0)
    return file_stream

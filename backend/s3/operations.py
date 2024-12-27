from io import BytesIO
from config.logger import logger
from .session import aioboto_session


@aioboto_session
async def create_bucket(s3_client, bucket_name: str = "bucket"):
    await s3_client.create_bucket(Bucket=bucket_name)

  
@aioboto_session
async def upload_file(
    filename: str,
    filepath: str,
    s3_client, 
    bucket_name: str = "bucket"):
    await s3_client.upload_file(
        filepath, 
        bucket_name, 
        filename
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

@aioboto_session
async def load_images_to_s3(s3_client):
    try:
        await s3_client.head_bucket(Bucket="bucket")
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            await s3_client.create_bucket(Bucket="bucket")
    try:
        await s3_client.head_object(Bucket="bucket", Key="image.png")
        logger.info(f"Файл уже существует в S3.")
    except s3_client.exceptions.ClientError as e:
        logger.info(f"Файл не найден в S3.")
        logger.error(e, exc_info=True)
        if e.response['Error']['Code'] == "404":
            await upload_file("image.png", "image.png")

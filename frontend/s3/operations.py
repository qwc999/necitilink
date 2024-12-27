from io import BytesIO
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
async def download_file(filename: str, s3_client, bucket_name: str = "bucket"):
    return await s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': filename},
                ExpiresIn=604000  # Время действия ссылки в секундах (максимум до 7 дней)
            )

import os


POSTGRES_USER = str(os.environ.get("POSTGRES_USER"))
POSTGRES_PASSWORD = str(os.environ.get("POSTGRES_PASSWORD"))
POSTGRES_DB = str(os.environ.get("POSTGRES_DB"))
REDIS_HOST = str(os.environ.get("REDIS_HOST"))
REDIS_PASSWORD = str(os.environ.get("REDIS_PASSWORD"))
MINIO_URL = str(os.environ.get("MINIO_URL"))
MINIO_ROOT_USER = str(os.environ.get("MINIO_ROOT_USER"))
MINIO_ROOT_PASSWORD = str(os.environ.get("MINIO_ROOT_PASSWORD"))
KAFKA_USERNAME = str(os.environ.get("KAFKA_BACKEND_USER"))
KAFKA_PASSWORD = str(os.environ.get("KAFKA_BACKEND_PASSWORD"))
DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
KAFKA_URL = str(os.environ.get("KAFKA_URL"))
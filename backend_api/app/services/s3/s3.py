import aioboto3
from fastapi import APIRouter, Body, UploadFile
ACCESS_KEY = 'ba88124bb9f211337bbc6c103330c249'
SECRET_KEY = '863ba92413967d939d8cd1296b9010d62099712bb76c44fde5ffcea771822180'
BUCKET_NAME = 'group25022025'
ENDPOINT = 'https://8721af4803f2c3c631a90d8b64d397b7.r2.cloudflarestorage.com'
# ---------------------------------------------------------------------------


PUBLIC_URL = 'https://pub-d2b580fe400441b19434564174b8efa7.r2.dev'


class  S3Storage:
    def __init__(self):
        self.bucket_name = BUCKET_NAME

    async def get_s3_session(self):
        session = aioboto3.Session()
        async with session.client(
            's3',
            endpoint_url=ENDPOINT,
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name='EEUR'
        ) as s3:
            yield s3

    async def upload_product_image(self, file: UploadFile, restaurant_uuid: str) -> str:
        async for s3_client in self.get_s3_session():
            path = f'products/{restaurant_uuid}/{file.filename}'
            await s3_client.upload_fileobj(file, self.bucket_name, path)
            url = f"{PUBLIC_URL}/{path}"
        return url

s3_storage = S3Storage()
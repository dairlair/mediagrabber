import boto3
from mediagrabber import StorageInterface
from typing import Optional
import io


class S3Storage(StorageInterface):
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str
    bucket: str
    host: Optional[str]

    def __init__(self, aws_access_key_id, aws_secret_access_key, region, bucket, host=None):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region = region
        self.bucket = bucket
        self.host = host

    def get_client(self):
        # config = Config(signature_version=botocore.UNSIGNED)
        return boto3.client('s3', aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)

    def save(self, data: bytes, key: str) -> str:
        client = self.get_client()
        client.upload_fileobj(io.BytesIO(data), self.bucket, key,
                              ExtraArgs={'ACL': 'public-read'})
        return f'https://{self.bucket}.s3.amazonaws.com/{key}'

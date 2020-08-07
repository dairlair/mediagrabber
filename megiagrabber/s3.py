import boto3
from botocore.config import Config

config = Config(
    region_name = 'us-east-1',
)

def save(file_name: str):
    s3 = boto3.client('s3', config=config, aws_access_key_id='AKIAIKOOWOEBPSHB5JZQ', aws_secret_access_key='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')
    with open(file_name, "rb") as f:
        result = s3.upload_fileobj(f, "mediagrabber-dev", file_name)
        print(result)
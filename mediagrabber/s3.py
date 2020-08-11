import boto3
from botocore.exceptions import NoCredentialsError
from mediagrabber import StorageInterface
from urllib.parse import urlparse


class S3Storage(StorageInterface):
    aws_access_key_id: str
    aws_secret_access_key: str
    region: str
    bucket: str
    """
    Accepts credentials and config for S3 compatible object storage in the URL format.
    URL must be in format:
        s3://<aws_access_key_id>:<aws_secret_access_key>@<host>/<region>/<bucket>
    """
    def __init__(self, url: str):
        parts = urlparse(url)
        self.aws_access_key_id = parts.username
        self.aws_secret_access_key = parts.password
        paths = parts.path.split('/')
        self.region = paths[0]
        self.bucket = paths[1] if len(paths) > 1 else None
        

    def save(self, content: bytes, name: str) -> str:
        return 'xxx'


# region = 'us-east-1'
# filepath = '/home/reskator/wr-720.sh-18.jpg'
# bucket = 'mediagrabber-dev'
# key = 'wr-720.sh-18.jpg'

s3://AKIAIKOOWOEBPSHB5JZQ:ja9cxuvd7RpfadVPGrbuAQyL3uLBwh2l22Kzq29x@


# def upload_to_aws(local_file, bucket, s3_file):
#     s3 = boto3.client('s3', aws_access_key_id='AKIAIKOOWOEBPSHB5JZQ',
#                       aws_secret_access_key='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')

#     try:
#         with open(local_file, 'rb') as data:
#             s3.upload_fileobj(data, bucket, key)
#         print("Upload Successful")

#         return True
#     except FileNotFoundError:
#         print("The file was not found")
#         return False
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False

# upload_to_aws(filepath, bucket, key)
from s3 import S3Storage
import uuid

aws_access_key_id = 'AKIAIKOOWOEBPSHB5JZQ'
aws_secret_access_key = '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'
region = 'us-east-1'
bucket = 'mediagrabber-dev'
filepath = '/home/reskator/wr-720.sh-18.jpg'

storage = S3Storage(aws_access_key_id, aws_secret_access_key, region, bucket)

with open(filepath, 'rb') as data:
    key: str = str(uuid.uuid4())
    url = storage.save(data, key)
    print(f'File saved and available with this url: {url}')

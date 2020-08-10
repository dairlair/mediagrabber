import boto3
from botocore.exceptions import NoCredentialsError

region = 'us-east-1'
filepath = '/home/reskator/wr-720.sh-18.jpg'
bucket = 'mediagrabber-dev'
key = 'wr-720.sh-18.jpg'


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id='AKIAIKOOWOEBPSHB5JZQ',
                      aws_secret_access_key='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')

    try:
        with open(local_file, 'rb') as data:
            s3.upload_fileobj(data, bucket, key)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

upload_to_aws(filepath, bucket, key)
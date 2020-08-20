from s3 import S3Storage
from framer import OpencvVideoFramesRetriever
from mediagrabber import MediaGrabber

aws_access_key_id = 'AKIAIKOOWOEBPSHB5JZQ'
aws_secret_access_key = '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'
region = 'us-east-1'
bucket = 'mediagrabber-dev'

storage = S3Storage(aws_access_key_id, aws_secret_access_key, region, bucket)
framer = OpencvVideoFramesRetriever('/tmp')
mg = MediaGrabber(framer, storage)

# url = 'https://rt.pornhub.com/view_video.php?viewkey=ph5ec22341819b1'
# urls = mg.grab(url)

# for url in urls:
#     print(url)

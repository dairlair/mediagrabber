import flask
from flask import request, jsonify
from flask_cors import CORS
import json
import os
import requests
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

app = flask.Flask(__name__)
CORS(app)

dapr_port = os.getenv('DAPR_HTTP_PORT', '3500')
dapr_url = f'http://localhost:{dapr_port}/v1.0'
dapr_pubsub_name = 'pubsub'


@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    subscriptions = [
        {
            'pubsubName': 'pubsub',
            'topic': 'VideoPageFound',
            'route': 'video-page-found'
        },
        {
            'pubsubName': 'pubsub',
            'topic': 'VideoGrabbed',
            'route': 'video-grabbed'
        }
    ]
    return jsonify(subscriptions)


@app.route('/video-page-found', methods=['POST'])
def video_page_found():
    # if True:
    #     return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

    url = request.json['data']['url']
    frames = mg.grab(url)
    payload = json.dumps({'url': url, 'frames': frames})
    url = f'{dapr_url}/publish/{dapr_pubsub_name}/VideoGrabbed'
    response = requests.post(url, json=payload)
    print(response)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/video-grabbed', methods=['POST'])
def video_grabbed():
    print(f'Video grabbed: {request.json}', flush=True)

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


app.run()

import flask
from flask import request, jsonify
from flask_cors import CORS
import json
import os
import requests

app = flask.Flask(__name__)
CORS(app)

dapr_port = os.environ('DAPR_HTTP_PORT', '3500')
dapr_url = f'http://localhost:${dapr_port}/v1.0'
dapr_pubsub_name = 'pubsub'


@app.route('/dapr/subscribe', methods=['GET'])
def subscribe():
    subscriptions = [{'pubsubName': 'pubsub', 'topic': 'A', 'route': 'A'}]
    return jsonify(subscriptions)


@app.route('/A', methods=['POST'])
def a_subscriber():
    print(f'A: {request.json}', flush=True)

    url = f'${dapr_url}/publish/${dapr_pubsub_name}/${req.body.messageType}'
    requests.post()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


app.run()

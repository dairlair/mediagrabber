import redis
import youtube_dl
import json

in_list_name = 'mediagrabber-in'
out_list_name = 'mediagrabber-out'
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

while True:
    x, message = r.blpop(in_list_name)
    data = json.loads(message)
    print(data)

    # get meta info from the video
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(data['url'], download=False)
        r.rpush(out_list_name, json.dumps(meta))
        print('Processed successfully')
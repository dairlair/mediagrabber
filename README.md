# MediaGrabber

[![codecov](https://codecov.io/gh/dairlair/mediagrabber/branch/master/graph/badge.svg?token=P76Zts58lp)](undefined)

The cloud native application for media grabbing. The application listens the specified queue with AMQP and expects messages in the format:
```json
{"url": "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"}
```

## Run, using CLI interface

Before using the MediaGrabber in the cloned repository you need to install [youtube-dl](https://github.com/ytdl-org/youtube-dl#installation).

Create local python environment with:
```sh
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

Now you can download video from the website with:
```sh
python mediagrabber/cli.py download "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"
python mediagrabber/cli.py download "https://pornhub.com/view_video.php?viewkey=ph5fcea9ba0ae13"
```

Retrieve faces from the downloaded video via:
```sh
python mediagrabber/cli.py retrieve /home/dairlair/Videos/Constantine.mkv
```

Or download, retrieve and save faces in one command with:
```sh
python mediagrabber/cli.py grab "https://pornhub.com/view_video.php?viewkey=ph5fcea9ba0ae13" --height=180
```
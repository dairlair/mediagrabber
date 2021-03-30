# MediaGrabber

[![codecov](https://codecov.io/gh/dairlair/mediagrabber/branch/master/graph/badge.svg?token=P76Zts58lp)](undefined)

The cloud native application for media grabbing. The application listens the specified queue with AMQP and expects messages in the format:
```json
{"url": "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"}
```

You can run the faces retrieving with customized params:
```json
{
    "url": "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309",
    "tolerance": 0.45
}
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
python app/cli/cli.py download "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"
python app/cli/cli.py download "https://pornhub.com/view_video.php?viewkey=ph5fcea9ba0ae13"
python app/cli/cli.py download "https://www.bloomberg.com/news/videos/2021-03-09/-bloomberg-the-open-full-show-03-09-2021-video"
```

Retrieve and save faces from the downloaded video via:
```sh
python app/cli/cli.py retrieve /home/dairlair/Videos/Constantine.mkv --resize_height=360
```

Or download, retrieve and save faces in one command with (just specify URL instead of existing file):
```sh
python app/cli/cli.py retrieve "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"
python app/cli/cli.py retrieve "https://pornhub.com/view_video.php?viewkey=ph5fcea9ba0ae13" --resize_height=180
```

### Download video, retrieve faces and calculate embeddings

```sh
python app/cli/cli.py memorize "https://www.pornhub.com/view_video.php?viewkey=ph5fd7bc93973ad" video test 1 publication
python app/cli/cli.py memorize "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309" video test 1 publication
# And mor than 44 minutes of breathtaking Bridgette B...
python app/cli/cli.py memorize "https://www.pornhub.com/view_video.php?viewkey=ph602eac372883c" video publication 2 publication,bridgette
```

```sql
CREATE TABLE urls (
  id BIGSERIAL PRIMARY KEY,
  URL TEXT NOT NULL,
  UNIQUE(url)
);

DROP TABLE IF EXISTS faces;
CREATE TABLE faces (
  id BIGSERIAL PRIMARY KEY,
  url_id BIGINT NOT NULL,
  ts FLOAT NOT NULL,
  face_id SMALLINT NOT NULL, -- An unique face number in the one frame
  box SMALLINT[4] NOT NULL, -- Face paddings, in the CSS format (top, right, bottom, left)
  entity TEXT NOT NULL DEFAULT '',
  entity_id BIGINT NOT NULL DEFAULT 0,
  tags TEXT[] NOT NULL DEFAULT '{}'::TEXT[],
  encoder VARCHAR(32) NOT NULL,
  encoding FLOAT[128],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
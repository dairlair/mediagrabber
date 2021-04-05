# MediaGrabber

[![codecov](https://codecov.io/gh/dairlair/mediagrabber/branch/master/graph/badge.svg?token=P76Zts58lp)](undefined)

The cloud native application for the face recognition from the media. 

For faces memorizing the application listens the specified queue (`mediagrabber.memorize`) through AMQP and expects messages in the format:
```json
{"url": "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"}
```

You can run the faces retrieving with customized params:
```json
{
    "url": "https://www.pornhub.com/view_video.php?viewkey=ph602eac372883c",
    "tolerance": 0.45,
    "source": "youtubedl", 
    "entity": "publication",
    "id": 2,
    "tags": ["publication","bridgette"]
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
python app/cli/cli.py memorize "https://www.pornhub.com/view_video.php?viewkey=ph5fd7bc93973ad" youtubedl publication 1 publication,tag1,tag2
python app/cli/cli.py memorize "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309" youtubedl publication 1 publication,tag1,tag2
# And mor than 44 minutes of breathtaking Bridgette B...
python app/cli/cli.py memorize "https://www.pornhub.com/view_video.php?viewkey=ph602eac372883c" youtubedl publication 2 publication,bridgette
# Or you can memorize the picture by the direct URL
# Photo with small faces:
python app/cli/cli.py memorize "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=687&q=100" direct publication 3 publication,unsplash
# Photo with big face:
python app/cli/cli.py memorize "https://images.unsplash.com/photo-1557296387-5358ad7997bb?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=694&q=80" direct publication 3 publication,unsplash
# Recognize faces:
python app/cli/cli.py memorize faceId
```

```sql
DROP TABLE IF EXISTS urls;
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
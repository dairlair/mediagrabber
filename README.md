# MediaGrabber

[![codecov](https://codecov.io/gh/dairlair/mediagrabber/branch/main/graph/badge.svg?token=P76Zts58lp)](undefined)
[![Open in Visual Studio Code](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/dairlair/mediagrabber)

The cloud native application for the face recognition from the media.

## Memorizing
For the faces memorizing the application listens the specified queue (`mediagrabber.memorize`, is configurable) through AMQP and expects messages in the format:
```json
{"url": "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"}
```

You can run the faces remorizing with customized params:
```json
{
    "url": "https://www.pornhub.com/view_video.php?viewkey=ph602eac372883c",
    "tolerance": 0.45,
    "downloader": "youtubedl", 
    "entity": "publication",
    "id": 2,
    "tags": ["publication","bridgette"]
}
```

The result will be published to the in format:
```json
{
    "id": 9, 
    "url": "https://edition.cnn.com/videos/politics/2021/05/19/jim-mcgovern-kevin-mccarthy-weak-january-6-commission-sot-vpx.cnn/video/playlists/this-week-in-politics/", "entity": "Investigation", 
    "tolerance": 0.45, 
    "tags": ["Investigation"], 
    "downloader": "youtubedl", 
    "success": true,
    "resolution": "File [https://edition.cnn.com/videos/politics/2021/05/19/jim-mcgovern-kevin-mccarthy-weak-january-6-commission-sot-vpx.cnn/video/playlists/this-week-in-politics/] memorized successfully", 
    "faces": [364, 365, 366]}
```


For the faces recogntion send this event to the queue `mediagrabber.recognize`:
```json
{"faceId": 1}
```

Or customized:
```json
{"faceId": 1, "count": 10, "tags": ["unsplash"]}
```

The response message example:
```json
{"faceId": 1, "count": 2, "success": true, "faces": [{"faceId": 1, "distance": 0.0}, {"faceId": 310, "distance": 0.0}]}
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
python app/cli/cli.py recognize 1 --count=10 --tags=unsplash
```

### Keira Knightley photos test:
```
python app/cli/cli.py memorize https://www.indiewire.com/wp-content/uploads/2018/01/keiraknightley.jpg direct "photo" 0 knightley
python app/cli/cli.py memorize https://www.indiewire.com/wp-content/uploads/2018/10/shutterstock_9933778ce.jpg direct "photo" 0 knightley
python app/cli/cli.py memorize "https://m.media-amazon.com/images/M/MV5BMTYwNDM0NDA3M15BMl5BanBnXkFtZTcwNTkzMjQ3OA@@._V1_UY317_CR6,0,214,317_AL_.jpg" direct  photo 0 knightley
python app/cli/cli.py recognize 3 --tolerance=0.5
```

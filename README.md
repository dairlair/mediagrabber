# MediaGrabber
The cloud native service for media grabbing

## How it works
MediaGrabber is created to help us analyze high video traffic flow from dozens of services.

The basic entity is the Video Page. Just an URL from any video service with unique video identifier like a https://www.youtube.com/watch?v=3AFTtiZVZ3o.

MediaGrabber uses queue to receive a new new URLs for processing and results publishing.

## Run with darp locally

```
dapr run --port 3500 --app-id mediagrabber --app-port 5000 python mediagrabber/app.py
dapr publish --pubsub "pubsub" --topic "VideoPageFound" --data '{"url": "https://rt.pornhub.com/view_video.php?viewkey=ph5b84c16b3e9a1"}'
# or another video
dapr publish --pubsub "pubsub" --topic "VideoPageFound" --data '{"url": "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"}'
# or
http POST http://localhost:3500/v1.0/publish/pubsub/VideoPageFound '{"url": "https://rt.pornhub.com/view_video.php?viewkey=ph5b84c16b3e9a1"}'
```
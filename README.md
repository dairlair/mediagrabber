# MediaGrabber
The cloud native service for media grabbing

## How it works
MediaGrabber is created to help us analyze high video traffic flow from dozens of services.

The basic entity is the Video Page. Just an URL from any video service with unique video identifier like a https://www.youtube.com/watch?v=3AFTtiZVZ3o.

MediaGrabber uses queue to receive a new new URLs for processing and results publishing.

You can easily add task for processing with:

```
redis-cli rpush mediagrabber-in '{"url":"https://www.youtube.com/watch?v=3AFTtiZVZ3o"}'
```
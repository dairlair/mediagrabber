# MediaGrabber
The cloud native service for media grabbing

## How it works
MediaGrabber is created to help us analyze high video traffic flow from dozens of services.

The basic entity is the Video Page. Just an URL from any video service with unique video identifier like a https://www.youtube.com/watch?v=3AFTtiZVZ3o.

MediaGrabber user can add URL for processing through REST API, described in Open API 3.0 format.

Just hit:
```shell script
curl -F "url=<Video Page URL>" http://localhost/add-url
```

During the processing of this request the MediaGrabber will add this URL to the Storage as a new URL (if it does not exist before) and returns success response.

If the URL is already exist in the Storage then MediaGrabber returns the status of this URL (new, processing, ready, failed).
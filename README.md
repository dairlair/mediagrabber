# MediaGrabber

[![codecov](https://codecov.io/gh/dairlair/mediagrabber/branch/master/graph/badge.svg?token=P76Zts58lp)](undefined)

The cloud native application for media grabbing. The application listens the specified queue with AMQP and expects messages in the format:
```json
{"url": "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"}
```
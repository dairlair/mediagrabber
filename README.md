# MediaGrabber
The cloud native service for media grabbing. The application listens the specified queue with AMQP and expects messages in the formt:
```json
{"url": "https://abcnews.go.com/Technology/video/california-judge-orders-uber-lyft-reclassify-drivers-employees-72302309"}
```
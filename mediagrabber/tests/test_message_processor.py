from mediagrabber.core import MediaGrabberError
from mediagrabber.consumer import MessageProcessor


# When message processed successfully
def test_message_processor_callback_returns_dictionary():
    # Given: callback returns valid dictionary
    response = {"data": "value"}

    def callback(service, payload):
        return response

    processor = MessageProcessor(None, callback)

    # When processing called
    payload = {"url": "https://example.com/file.mp4"}
    result = processor.process(payload)

    # Then returns merged payload and callback response
    assert result == {**payload, **response, "success": True}


# When message processed with MediaGrabberError
def test_message_processor_callback_raises_expected_error():
    # Given: callback raises MediaGrabberError
    def callback(service, payload):
        raise MediaGrabberError({"code": 128})

    processor = MessageProcessor(None, callback)

    # When processing called
    payload = {"url": "https://example.com/file.mp4"}
    result = processor.process(payload)

    # Then returns merged payload and callback response
    assert result == {
        **payload,
        "success": False,
        "error": {"data": {"code": 128}},
    }

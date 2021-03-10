import fire
from injector import Injector
from mediagrabber.dependencies import configure
from mediagrabber.core import MediaGrabber
import logging
from mediagrabber.config import Config

if __name__ == "__main__":
    # Set desired logging level
    logging.basicConfig(level=Config.log_level())

    # Dependency Injection setup
    injector = Injector([configure])

    service: MediaGrabber = injector.get(MediaGrabber)
    fire.Fire(service)

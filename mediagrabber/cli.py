import fire
from injector import Injector
from mediagrabber.dependencies import configure
from mediagrabber.core import MediaGrabber

if __name__ == "__main__":
    # Dependency Injection setup
    injector = Injector([configure])
    service: MediaGrabber = injector.get(MediaGrabber)
    fire.Fire(service)

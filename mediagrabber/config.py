import os


class Config():
    # AMQP settings
    @staticmethod
    def amqp_url() -> str:
        return os.environ.get('AMQP_URL') or 'amqp://ia:ia@host.docker.internal:5672/iavhost'

    @staticmethod
    def queue_in() -> str:
        return os.environ.get('IN') or 'mediagrabber.in'

    @staticmethod
    def queue_out() -> str:
        return os.environ.get('OUT') or 'mediagrabber.out'

import os


class Config():
    # Core settings
    @staticmethod
    def workdir() -> str:
        return os.environ.get('WORKDIR') or 'workdir'

    @staticmethod
    def log_level() -> str:
        return os.environ.get('LOG_LEVEL') or 'WARNING'

    # AMQP settings
    @staticmethod
    def amqp_url() -> str:
        return os.environ.get('AMQP_URL') or 'amqp://ia:ia@host.docker.internal:5672/iavhost'

    @staticmethod
    def queue_in() -> str:
        return os.environ.get('AMQP_IN') or 'mediagrabber.in'

    @staticmethod
    def queue_out() -> str:
        return os.environ.get('AMQP_OUT') or 'mediagrabber.out'

    # AWS Settings
    @staticmethod
    def aws_access_key_id() -> str:
        return Config.require('AWS_ACCESS_KEY_ID')

    @staticmethod
    def aws_secret_access_key() -> str:
        return Config.require('AWS_SECRET_ACCESS_KEY')

    @staticmethod
    def aws_region() -> str:
        return Config.require('AWS_REGION')

    @staticmethod
    def aws_bucket() -> str:
        return Config.require('AWS_BUCKET')

    @staticmethod
    def require(variable) -> str:
        value = os.environ.get(variable, None)
        if value is None:
            raise EnvironmentError("%s Must be specified" % variable)
        return value

import os
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
load_dotenv()


class Config:
    # Core settings
    @staticmethod
    def workdir() -> str:
        return os.environ.get("WORKDIR", "workdir")

    @staticmethod
    def log_level() -> str:
        return os.environ.get("LOG_LEVEL", "WARNING")

    # AMQP settings
    @staticmethod
    def amqp_url() -> str:
        default = "amqp://guest:guest@host.docker.internal:5672/%2f"
        return os.environ.get("AMQP_URL", default)

    @staticmethod
    def queue_in() -> str:
        return os.environ.get("AMQP_IN", "mediagrabber.in")

    @staticmethod
    def queue_out() -> str:
        return os.environ.get("AMQP_OUT", "mediagrabber.out")

    # AWS Settings
    @staticmethod
    def aws_access_key_id() -> str:
        return Config.require("AWS_ACCESS_KEY_ID")

    @staticmethod
    def aws_secret_access_key() -> str:
        return Config.require("AWS_SECRET_ACCESS_KEY")

    @staticmethod
    def aws_region() -> str:
        return Config.require("AWS_DEFAULT_REGION")

    @staticmethod
    def aws_bucket() -> str:
        return Config.require("AWS_BUCKET")

    @staticmethod
    def meter_dsn() -> str:
        return os.environ.get("METER_DSN")

    @staticmethod
    def require(variable) -> str:
        value = os.environ.get(variable, None)
        if value is None:
            raise EnvironmentError("%s Must be specified" % variable)
        return value

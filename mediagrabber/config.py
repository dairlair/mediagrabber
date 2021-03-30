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

    # RDBMS DSN
    @staticmethod
    def dsn() -> str:
        default = "postgresql://mediagrabber:mediagrabber@localhost:5432/mediagrabber"
        return os.environ.get("DSN", default)

    # AMQP settings
    @staticmethod
    def amqp_url() -> str:
        default = "amqp://guest:guest@localhost:5672/%2f"
        return os.environ.get("AMQP_URL", default)

    @staticmethod
    def queue_in() -> str:
        return os.environ.get("AMQP_IN", "mediagrabber.in")

    @staticmethod
    def queue_out() -> str:
        return os.environ.get("AMQP_OUT", "mediagrabber.out")

    @staticmethod
    def require(variable) -> str:
        value = os.environ.get(variable, None)
        if value is None:
            raise EnvironmentError("%s Must be specified" % variable)
        return value

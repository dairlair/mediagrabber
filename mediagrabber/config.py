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
    def queue_memorize() -> str:
        return os.environ.get("AMQP_MEMORIZE", "mediagrabber.memorize")

    @staticmethod
    def queue_memorized() -> str:
        return os.environ.get("AMQP_MEMORIZED", "mediagrabber.memorized")

    @staticmethod
    def require(variable) -> str:
        value = os.environ.get(variable, None)
        if value is None:
            raise EnvironmentError("%s Must be specified" % variable)
        return value

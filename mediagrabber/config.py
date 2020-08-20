from os import getenv


class Config():
    @staticmethod
    def get_dapr_port() -> str:
        return getenv('DAPR_PORT')
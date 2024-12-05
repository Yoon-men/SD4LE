from etc.config import Config

from func.DB_manager import DBManager

# * ------------------------------------------------------------ *#


class SD4LEConfig(Config):
    DB_manager = DBManager()

    @classmethod
    def check_version(cls) -> bool:
        latest_version = cls.DB_manager.get_latest_version()
        return True if cls.VERSION >= latest_version else False
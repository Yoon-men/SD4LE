"""
Config

ver 1.0.2

~ 02:56 on Sun, Dec 8, 2024 ~
"""

# * ------------------------------------------------------------ *#

import os
import sys
import pickle
from typing import Dict
import traceback

import certifi

import platform

# * ------------------------------------------------------------ *#

from etc.logger import *

# * ------------------------------------------------------------ *#


class Config:
    VERSION: str = "1.3.0"
    LAST_UPDATED: str = "Sun, Dec 8, 2024"

    def get_base_path() -> str:
        if getattr(sys, "frozen", False):
            # PyInstaller
            if hasattr(sys, "_MEIPASS"):
                return sys._MEIPASS
            # py2app
            else:
                return os.path.join(os.path.dirname(sys.executable), "..", "Resources")
        else:
            return os.getcwd()

    FONT_PATH: str = os.path.join(get_base_path(), "src", "NanumGothicBold.otf")

    ICON_PATH: str = os.path.join(get_base_path(), "src", f"Icon.{'ico' if platform.system() == 'Windows' else 'icns'}")

    SVG_PATH: str = os.path.join(get_base_path(), "src", "img", "loading.svg")

    ENV_PATH: str = os.path.join(get_base_path(), ".env")

    logger = init_logger(
        name="Sandevistan for labsafety education",
        version=VERSION,
        c_level=DEBUG,
        f_level=INFO,
        f_path="./log",
    )

    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1.0"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1.0"
    os.environ["QT_SCALE_FACTOR"] = "1.0"

    os.environ["SSL_CERT_FILE"] = certifi.where()

    DATA_PATH: str = "data.dat"
    DATA: Dict = {}

    @classmethod
    def save_data(cls) -> None:
        with open(cls.DATA_PATH, "wb") as f:
            pickle.dump(cls.DATA, f)

        return

    @classmethod
    def load_data(cls) -> bool:
        if not os.path.isfile(cls.DATA_PATH):
            return False

        try: 
            with open(cls.DATA_PATH, "rb") as f:
                cls.DATA: Dict = pickle.load(f)
        except: 
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
            exc_msg = "".join(formatted_traceback)

            cls.logger.error(f"Error occured while loading the data:\n{exc_msg}")
            return False
        
        return True
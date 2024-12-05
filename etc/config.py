"""
Config

ver 1.0.1

~ Wed, Nov 27, 2024 ~
"""

# * ------------------------------------------------------------ *#

import os
import sys
import pickle
from typing import Dict
import traceback

import certifi

# * ------------------------------------------------------------ *#

from etc.logger import *

# * ------------------------------------------------------------ *#


class Config:
    VERSION: str = "1.2.1-alpha.1"
    LAST_UPDATED: str = "Thu, Dec 5, 2024"

    FONT_PATH: str = (
        os.path.join(sys._MEIPASS, "src", "NanumGothicBold.otf")
        if getattr(sys, "frozen", False)
        else os.path.join(os.getcwd(), "src", "NanumGothicBold.otf")
    )

    ICON_PATH: str = (
        os.path.join(sys._MEIPASS, "src", "Icon.ico")
        if getattr(sys, "frozen", False)
        else os.path.join(os.getcwd(), "src", "Icon.ico")
    )

    SVG_PATH: str = (
        os.path.join(sys._MEIPASS, "src", "img", "loading.svg")
        if getattr(sys, "frozen", False)
        else os.path.join(os.getcwd(), "src", "img", "loading.svg")
    )

    ENV_PATH: str = (
        os.path.join(sys._MEIPASS, ".env")
        if getattr(sys, "frozen", False)
        else os.path.join(os.getcwd(), ".env")
    )

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
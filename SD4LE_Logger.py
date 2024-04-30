"""
SD4LE, Sandevistan for labsafety education

ver 1.0.0

~ Tue, Apr 30, 2024 ~
"""

#* ------------------------------------------------------------ *#

import logging

from os import (
    path     as os_path, 
    makedirs as os_makedirs
)

import time

#* ------------------------------------------------------------ *#

DEBUG    = logging.DEBUG
INFO     = logging.INFO
WARNING  = logging.WARNING
ERROR    = logging.ERROR
CRITICAL = logging.CRITICAL

#* ------------------------------------------------------------ *#

def init_logger(
    name: str, version: str, c_level: int, f_level: int, f_path: str = "./SD4LE_log"
) -> logging.Logger: 
    logger = logging.getLogger(name=name)
    logger.setLevel(DEBUG)
    logger.propagate = False

    if not os_path.isdir(f_path): 
        os_makedirs(f_path)
    
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(
        filename=f"{f_path}/{time.strftime('%Y-%m-%d')}.log", encoding="utf-8"
    )
    c_handler.setLevel(c_level)
    f_handler.setLevel(f_level)

    c_format = logging.Formatter(
        "[ver %(_version)s|%(levelname)8s] %(asctime)s - %(message)s", 
        defaults={"_version": version}
    )
    f_format = logging.Formatter(
        "[ver %(_version)s|%(levelname)8s] %(asctime)s - %(message)s", 
        defaults={"_version": version}
    )
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

    # --- End of logger() --- #
"""
Logger

- DEBUG    = logging.DEBUG
- INFO     = logging.INFO
- WARNING  = logging.WARNING
- ERROR    = logging.ERROR
- CRITICAL = logging.CRITICAL
- init_logger(name: str, version: str, c_level: int, f_level: int, f_path: str = "./log") -> logging.Logger

ver 1.1.1

~ Tue, Sep 24, 2024 ~
"""

#* ------------------------------------------------------------ *#

import logging
import os
import time

#* ------------------------------------------------------------ *#

DEBUG    = logging.DEBUG
INFO     = logging.INFO
WARNING  = logging.WARNING
ERROR    = logging.ERROR
CRITICAL = logging.CRITICAL

#* ------------------------------------------------------------ *#

def init_logger(
        name: str, version: str, c_level: int, f_level: int, f_path: str = "./log"
) -> logging.Logger: 
    logger = logging.getLogger(name=name)
    logger.setLevel(DEBUG)
    logger.propagate = False

    if not os.path.isdir(f_path): 
        os.makedirs(f_path)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(
        filename=f"{f_path}/{time.strftime('%Y-%m-%d')}.log", 
        encoding="utf-8"
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
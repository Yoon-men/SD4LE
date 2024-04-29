"""
SD4LE, Sandevistan for labsafety education

ver 0.0.2

~ Mon, Apr 29, 2024 ~
"""

#* ------------------------------------------------------------ *#

import logging
import sys
import os
from typing import List
import traceback

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QThread, QObject, Signal

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
from chromedriver_autoinstaller import (
    install as install_chromedriver,
    get_chrome_version,
)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    JavascriptException,
    NoAlertPresentException,
)

from SD4LE_UI_Main import MainUI
from SD4LE_UI_Alert import AlertUI
from SD4LE_UI_Loading import LoadingUI

#* ------------------------------------------------------------ *#

class Main(QObject) : 
    def __init__(self, app: QApplication): 
        super().__init__()

        ## UIs
        global mainUI, alertUI, loadingUI
        mainUI = MainUI()
        alertUI = AlertUI()
        loadingUI = LoadingUI()

        ## Sandevistan Operating Thread
        global QOperatingThread, operatingThread
        QOperatingThread = QThread()
        QOperatingThread.start()
        operatingThread = OperatingThread()
        operatingThread.moveToThread(QOperatingThread)

        mainUI.show()
        self.signal()
        sys.exit(app.exec_())

        # --- End of __init__() --- #
    

    def signal(self) -> None: 
        ## Main UI
        mainUI.login_BT.clicked.connect(operatingThread.operate)


        ## Sandevistan Operating Thread
        operatingThread.error_occured_signal.connect(self.alert)
        operatingThread.close_loading_window_signal.connect(loadingUI.close)

        
        # --- End of signal() --- #
    


    def alert(self, msg: str) -> None: 
        alertUI.description_LB.setText(msg)
        alertUI.exec_()
        
        # --- End of alert() --- #
    
    ## --- End of Main --- ##




class OperatingThread(QObject): 
    error_occured_signal = Signal(str)
    close_loading_window_signal = Signal()

    def operate(self) -> int: 
        if (mainUI.userID_LE.text() == '') or (mainUI.userPW_LE.text() == ''): 
            self.error_occured_signal.emit("ID, PW가 모두 입력되었는지\n확인해 주십시오.")
            return 0
            
        pass                # Test code / please delete this line.

        # --- End of operate() --- #

    ## --- End of OperatingThread --- ##




def launch() -> None : 
    app = QApplication(sys.argv)
    Main(app)

    # --- End of launch() --- #





if __name__ == "__main__" : 
    launch()
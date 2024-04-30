"""
SD4LE, Sandevistan for labsafety education

ver 1.0.0

~ Tue, Apr 30, 2024 ~
"""

#* ------------------------------------------------------------ *#

import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QThread, QObject, Signal, QCoreApplication

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
from chromedriver_autoinstaller import (
    install as install_chromedriver,
    get_chrome_version,
)

from SD4LE_UI_Main import MainUI
from SD4LE_UI_Alert import AlertUI
from SD4LE_UI_Loading import LoadingUI
from SD4LE_Logger import *
from SD4LE_KeyFn import Sandevistan
from SD4LE_Encryption import *

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
        ## Exit
        QCoreApplication.instance().aboutToQuit.connect(self.quit)

        ## Main UI
        mainUI.login_BT.clicked.connect(operatingThread.operate)
        mainUI.userPW_LE.returnPressed.connect(operatingThread.operate)


        ## Sandevistan Operating Thread
        operatingThread.show_loading_window_signal.connect(loadingUI.exec_)
        operatingThread.alert_occured_signal.connect(self.alert)
        operatingThread.close_loading_window_signal.connect(loadingUI.close)

        
        # --- End of signal() --- #
    

    def quit(self) -> None: 
        QOperatingThread.quit()
        QCoreApplication.instance().quit()

        # --- End of quit() --- #



    def alert(self, msg: str) -> None: 
        loadingUI.close()

        alertUI.description_LB.setText(msg)
        alertUI.exec_()
        
        # --- End of alert() --- #
    
    ## --- End of Main --- ##




class OperatingThread(QObject): 
    show_loading_window_signal = Signal()
    alert_occured_signal = Signal(str)
    close_loading_window_signal = Signal()

    def operate(self) -> int: 
        logger.info("START: 산데비스탄 가동")
        self.show_loading_window_signal.emit()

        if (mainUI.userID_LE.text() == '') or (mainUI.userPW_LE.text() == ''): 
            self.alert_occured_signal.emit("ID, PW가 모두 입력되었는지\n확인해 주세요.")
            logger.warning("STOP : 산데비스탄 가동 중지(사용자 계정 정보 미입력)")
            return 1
        
        if not mainUI.userID_LE.text() in load_and_decryption().split('\n'): 
            self.alert_occured_signal.emit("프로그램 사용 권한이 없습니다.\n개발자에게 문의하세요.")
            logger.warning("STOP : 산데비스탄 가동 중지(사용 권한 미보유)")
            return 1
        
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{get_chrome_version()} Safari/537.36")
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])

        chrome_service = Service(install_chromedriver())
        chrome_service.creation_flags = CREATE_NO_WINDOW
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.implicitly_wait(2)

        sandevistan = Sandevistan(driver, logger)

        if sandevistan.this_fffire(): 
            logger.error("STOP : 산데비스탄 가동 중지(this_fffire)")
            return 1
        if sandevistan.whos_ready_for_tomorrow(mainUI.userID_LE.text(), mainUI.userPW_LE.text()): 
            self.alert_occured_signal.emit("잘못된 계정 정보입니다.\nID와 PW를 다시 확인해 주세요.")
            logger.warning("STOP : 산데비스탄 가동 중지(whos_ready_for_tomorrow)")
            return 1
        if sandevistan.friday_night_fire_fight(): 
            logger.error("STOP : 산데비스탄 가동 중지(friday_night_fire_fight)")
            return 1
        if sandevistan.i_really_want_to_stay_at_your_house(): 
            logger.error("STOP : 산데비스탄 가동 중지(i_really_want_to_stay_at_your_house)")
            return 1
        if sandevistan.let_you_down(): 
            logger.error("STOP : 산데비스탄 가동 중지(let_you_down)")
            return 1


        self.close_loading_window_signal.emit()
        logger.info("E N D: 산데비스탄 완료")
        self.alert_occured_signal.emit("작업을 완료했습니다.")

        # --- End of operate() --- #

    ## --- End of OperatingThread --- ##




def launch() -> None : 
    global logger
    logger = init_logger(
        name="Sandevistan for labsafety education", 
        version="1.0.0", 
        c_level=DEBUG, 
        f_level=INFO,
        f_path="./SD4LE_log"
    )

    app = QApplication(sys.argv)
    Main(app)

    # --- End of launch() --- #





if __name__ == "__main__" : 
    launch()
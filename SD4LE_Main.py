"""
SD4LE, Sandevistan for labsafety education

ver 1.1.0

~ Thu, May 2, 2024 ~
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
from SD4LE_Version_Checker import version_check

#* ------------------------------------------------------------ *#

version = "1.1.0"

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

        version_check_res = version_check(version)
        if version_check_res: 
            alertUI.github_ok_BT.show()
            self.alert(version_check_res)

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


    def operate(self) -> int: 
        logger.info("START: 산데비스탄 가동")
        self.show_loading_window_signal.emit()

        if (mainUI.userID_LE.text() == '') or (mainUI.userPW_LE.text() == ''): 
            self.alert_occured_signal.emit("ID, PW가 모두 입력되었는지\n확인해 주세요.")
            logger.warning("STOP : 산데비스탄 가동 중지 (사용자 계정 정보 미입력)")
            return 1

        user_check_res = user_check(mainUI.userID_LE.text())
        if user_check_res: 
            self.alert_occured_signal.emit(user_check_res)
            logger.warning("STOP : 산데비스탄 가동 중지 (user_check)")
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

        sandevistan = Sandevistan(driver, logger, mainUI.userID_LE.text(), mainUI.userPW_LE.text())

        cheap_but_similar = {
            "this_fffire"                        : "STOP : 산데비스탄 가동 중지 (this_fffire)",
            "whos_ready_for_tomorrow"            : "STOP : 산데비스탄 가동 중지 (whos_ready_for_tomorrow)",
            "friday_night_fire_fight"            : "STOP : 산데비스탄 가동 중지 (friday_night_fire_fight)",
            "i_really_want_to_stay_at_your_house": "STOP : 산데비스탄 가동 중지 (i_really_want_to_stay_at_your_house)",
            "let_you_down"                       : "STOP : 산데비스탄 가동 중지 (let_you_down)"
        }

        for function, message in cheap_but_similar.items():
            res = getattr(sandevistan, function)()
            if res:
                self.alert_occured_signal.emit(res)
                logger.error(message)
                return 1


        self.alert_occured_signal.emit("작업을 완료했습니다.")
        logger.info("E N D: 산데비스탄 완료")

        # --- End of operate() --- #

    ## --- End of OperatingThread --- ##





def launch() -> None : 
    global logger
    logger = init_logger(
        name="Sandevistan for labsafety education", 
        version="1.1.0", 
        c_level=DEBUG, 
        f_level=INFO,
        f_path="./SD4LE_log"
    )

    app = QApplication(sys.argv)
    Main(app)

    # --- End of launch() --- #


if __name__ == "__main__" : 
    launch()
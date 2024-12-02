"""
SD4LE, Sandevistan for labsafety education

ver 1.2.0

~ Tue, Dec 3, 2024 ~
"""

#* ------------------------------------------------------------ *#

import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, QObject, Signal, QCoreApplication

from threading import Thread

#* ------------------------------------------------------------ *#

from SD4LE_config import SD4LEConfig

from UI.UI_Main import MainUI
from UI.UI_Alert import AlertUI
from UI.UI_Loading import LoadingUI

from func.operation import Operation

#* ------------------------------------------------------------ *#


class Main(QObject) : 
    def __init__(self, app: QApplication): 
        super().__init__()

        self.app = app
        self.app.setApplicationName("SD4LE")

        ## UI
        self.mainUI = MainUI()
        self.mainUI.show()

        self.alertUI = AlertUI()

        self.loadingUI = LoadingUI()


        ## Func
        self.operation_thread = QThread()
        self.operation_thread.start()
        self.operation = Operation()
        self.operation.moveToThread(self.operation_thread)


        ## Version Check
        self.version_check: bool = SD4LEConfig.check_version()
        if not self.version_check:
            self.open_version_check_window()


        ## Signal
        self.signal()


        sys.exit(app.exec())

        # --- End of __init__() --- #


    def signal(self) -> None: 
        ## Exit
        QCoreApplication.instance().aboutToQuit.connect(self.quit)

        ## Main UI
        if self.version_check:
            self.mainUI.login_BT.clicked.connect(lambda: Thread(target=self.operation.run, args=(self.mainUI.userID_LE.text(), self.mainUI.userPW_LE.text())).start())
            self.mainUI.userPW_LE.returnPressed.connect(lambda: Thread(target=self.operation.run, args=(self.mainUI.userID_LE.text(), self.mainUI.userPW_LE.text())).start())
        else:
            self.mainUI.login_BT.clicked.connect(self.open_version_check_window)
            self.mainUI.userPW_LE.returnPressed.connect(self.open_version_check_window)


        ## Sandevistan Operating Thread
        self.operation.show_loading_window_signal.connect(self.loadingUI.exec)
        self.operation.open_alert_window_signal.connect(self.alert)
        
        # --- End of signal() --- #



    def quit(self) -> None: 
        self.operation_thread.quit()
        QCoreApplication.instance().quit()

        # --- End of quit() --- #



    def alert(self, msg: str) -> None: 
        self.loadingUI.close()

        self.alertUI.description_LB.setText(msg)
        self.alertUI.exec()
        
        # --- End of alert() --- #



    def open_version_check_window(self) -> None:
        latest_version = SD4LEConfig.DB_manager.get_latest_version()
        self.alertUI.github_ok_BT.show()
        self.alert(f"v{latest_version}이 출시되었습니다.\n이전 버전은 사용할 수 없습니다.")

    
    ## --- End of Main --- ##


# * ------------------------------------------------------------ *#


def launch() -> None : 
    app = QApplication(sys.argv)
    Main(app)

    # --- End of launch() --- #





if __name__ == "__main__" : 
    launch()
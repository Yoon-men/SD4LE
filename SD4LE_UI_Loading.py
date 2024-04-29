"""
SD4LE, Sandevistan for labsafety education

ver 0.0.2

~ Mon, Apr 29, 2024 ~
"""

#* ------------------------------------------------------------ *#

import sys
from enum import Enum
from os import path as os_path

from PySide2.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QGraphicsDropShadowEffect, 
)
from PySide2.QtCore import Qt, QSize, QEvent
from PySide2.QtGui import QIcon, QFontDatabase, QFont, QKeyEvent
from PySide2.QtSvg import QSvgWidget

from src.src import *

#* ------------------------------------------------------------ *#


class StyleSheets(Enum): 
    body_frame = """
        QFrame{
            background-color: #fafafa;
            border-radius: 10px;
        }
    """

    title_frame = """
        QFrame{
            background-color: #484848;
            border-radius: 10px;
        }
    """

    label = """
        QLabel{
            color: #545454;
        }
    """

    push_button = """
        QPushButton{
            background-color: #fafafa;
            border: 2px solid #aaaaaa;
            border-radius: 5px;
            color: #222222;
        }
        QPushButton:hover{
            background-color: #aaaaaa;
            color: #222222;
        }
    """

    # --- End of StyleSheets --- #




class LoadingUI(QDialog): 
    def __init__(self): 
        super().__init__()

        self.loadingUI()



    def loadingUI(self): 
        # Basic part
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(371, 250)
        self.setWindowTitle("SD4LE_Loading")
        icon_path = os_path.join(os_path.dirname(__file__), "SD4LE.ico")
        if os_path.isfile(icon_path): 
            self.setWindowIcon(QIcon(icon_path))
        font_path = os_path.join(os_path.dirname(__file__), "NanumGothicBold.otf")
        if os_path.isfile(font_path): 
            QFontDatabase.addApplicationFont(font_path)


        # Body part
        self.body_FRM = QFrame(self)
        self.body_FRM.setGeometry(10, 10, 351, 230)
        self.body_FRM.setStyleSheet(StyleSheets.body_frame.value)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(18)
        self.shadow.setOffset(0, 0)
        self.body_FRM.setGraphicsEffect(self.shadow)

        self.title_FRM = QFrame(self.body_FRM)
        self.title_FRM.setGeometry(0, -2, 351, 41)
        self.title_FRM.setStyleSheet(StyleSheets.title_frame.value)
        self.title_FRM.mousePressEvent = self.setCenterPoint
        self.title_FRM.mouseMoveEvent = self.moveWindow

        self.title_LB = QLabel(self.title_FRM)
        self.title_LB.setGeometry(90, 13, 170, 20)
        self.title_LB.setStyleSheet("""
            QLabel{
                image: url(:/src/loading_title.png);
            }
        """)

        svg_path = os_path.join(os_path.dirname(__file__), "src/loading.svg")
        if os_path.isfile(svg_path): 
            self.loading_SVG = QSvgWidget(svg_path, self.body_FRM)
            self.loading_SVG.setGeometry(136, 70, 80, 80)
        
        self.description_LB = QLabel(self.body_FRM)
        self.description_LB.setGeometry(71, 150, 210, 40)
        self.description_LB.setFont(QFont("나눔고딕OTF", 12, QFont.Bold))
        self.description_LB.setStyleSheet(StyleSheets.label.value)
        self.description_LB.setText("작업 진행 중")
        self.description_LB.setAlignment(Qt.AlignCenter)



    def setCenterPoint(self, event): 
        self.centerPoint = event.globalPos()

    def moveWindow(self, event): 
        if event.buttons() == Qt.LeftButton: 
            self.move(self.pos() + event.globalPos() - self.centerPoint)
            self.centerPoint = event.globalPos()
    


    def keyPressEvent(self, event): 
        if event.key() == Qt.Key_Escape: pass





if __name__ == "__main__": 
    app = QApplication(sys.argv)
    loadingUI = LoadingUI()
    loadingUI.show()
    sys.exit(app.exec_())
import sys
from enum import Enum
import os

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QLabel,
    QGraphicsDropShadowEffect, 
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon, QFontDatabase, QFont, QMouseEvent, QKeyEvent
from PySide6.QtSvgWidgets import QSvgWidget

# * ------------------------------------------------------------ *#

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# * ------------------------------------------------------------ *#

from SD4LE_config import SD4LEConfig

from src.img.img import *

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
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            border-bottom-left-radius: 0px;
            border-bottom-right-radius: 0px;
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

        # --- End of __init__() --- #



    def loadingUI(self): 
        # Basic part
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(371, 250)
        self.setWindowTitle("SD4LE_Loading")
        icon_path = SD4LEConfig.ICON_PATH
        if os.path.isfile(icon_path): 
            self.setWindowIcon(QIcon(icon_path))
        font_path = SD4LEConfig.FONT_PATH
        if os.path.isfile(font_path): 
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
                image: url(:/img/loading_title.png);
            }
        """)

        svg_path = SD4LEConfig.SVG_PATH
        if os.path.isfile(svg_path): 
            self.loading_SVG = QSvgWidget(svg_path, self.body_FRM)
            self.loading_SVG.setGeometry(136, 70, 80, 80)
        
        self.description_LB = QLabel(self.body_FRM)
        self.description_LB.setGeometry(71, 150, 210, 40)
        self.description_LB.setFont(QFont("나눔고딕OTF", 12, QFont.Weight.Bold))
        self.description_LB.setStyleSheet(StyleSheets.label.value)
        self.description_LB.setText("작업 진행 중")
        self.description_LB.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- End of loadingUI() --- #



    def setCenterPoint(self, event: QMouseEvent) -> None: 
        self.centerPoint: QPoint = event.globalPos()

        # --- End of setCenterPoint() --- #


    def moveWindow(self, event: QMouseEvent) -> None: 
        if event.buttons() == Qt.MouseButton.LeftButton: 
            self.move(self.pos() + event.globalPos() - self.centerPoint)
            self.centerPoint: QPoint = event.globalPos()

        # --- End of moveWindow() --- #



    def keyPressEvent(self, event: QKeyEvent) -> None: 
        if event.key() == Qt.Key.Key_Escape: pass

        # --- End of keyPressEvent() --- #
    
    ## --- End of LoadingUI() --- ##





if __name__ == "__main__": 
    app = QApplication(sys.argv)
    loadingUI = LoadingUI()
    loadingUI.show()
    sys.exit(app.exec())
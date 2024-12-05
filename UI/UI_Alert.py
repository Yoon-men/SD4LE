import sys
from enum import Enum
import os
from webbrowser import open as open_webbrowser

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QLabel,
    QPushButton,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon, QFontDatabase, QFont, QMouseEvent, QKeyEvent, QPalette, QColor

#* ------------------------------------------------------------ *#

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




class AlertUI(QDialog): 
    def __init__(self): 
        super().__init__()

        self.alertUI()
        self.signal()

        # --- End of __init__() --- #



    def alertUI(self): 
        # Basic part
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(371, 250)
        self.setWindowTitle("SD4LE_Alert")
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
                image: url(:/img/alert_title.png);
            }
        """)

        self.description_LB = QLabel(self.body_FRM)
        self.description_LB.setGeometry(26, 71, 300, 100)
        self.description_LB.setFont(QFont("나눔고딕OTF", 12, QFont.Weight.Bold))
        self.description_LB.setStyleSheet(StyleSheets.label.value)
        self.description_LB.setText("ID, PW가 모두 입력되었는지\n확인해 주십시오.")
        self.description_LB.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ok_BT = QPushButton(self.body_FRM)
        self.ok_BT.setGeometry(96, 199, 160, 24)
        self.ok_BT.setFont(QFont("나눔고딕OTF", 9, QFont.Weight.Bold))
        self.ok_BT.setStyleSheet(StyleSheets.push_button.value)
        self.ok_BT.setText("확인")
        self.ok_BT.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.github_ok_BT = QPushButton(self.body_FRM)
        self.github_ok_BT.setGeometry(96, 199, 160, 24)
        self.github_ok_BT.setFont(QFont("나눔고딕OTF", 9, QFont.Weight.Bold))
        self.github_ok_BT.setStyleSheet(StyleSheets.push_button.value)
        self.github_ok_BT.setText("확인")
        self.github_ok_BT.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.github_ok_BT.hide()

        # --- End of alertUI() --- #



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



    def signal(self) -> None: 
        self.ok_BT.clicked.connect(self.close)

        self.github_ok_BT.clicked.connect(lambda: open_webbrowser("https://github.com/Yoon-men/SD4LE/releases/latest/"))
        self.github_ok_BT.clicked.connect(self.github_ok_BT.hide)
        self.github_ok_BT.clicked.connect(self.close)

        # --- End of signal() --- #
    
    ## --- End of AlertUI() --- ##





if __name__ == "__main__": 
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # 라이트 모드 팔레트 설정
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))          # 창 배경 색상
    palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))            # 창 텍스트 색상
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))            # 입력 위젯의 배경 색상
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))   # 대체 배경 색상
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))     # 툴팁 배경 색상
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))           # 툴팁 텍스트 색상
    palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))                  # 일반 텍스트 색상
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))          # 버튼 배경 색상
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))            # 버튼 텍스트 색상
    palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))          # 강조된 텍스트 색상
    palette.setColor(QPalette.ColorRole.Link, QColor(0, 0, 255))                # 링크 색상
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))         # 선택 항목 강조 색상
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255)) # 선택 항목 텍스트 색상

    # 팔레트 적용
    app.setPalette(palette)

    alertUI = AlertUI()
    alertUI.show()
    sys.exit(app.exec())
import sys
from enum import Enum
import os

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFontDatabase, QFont, QPalette, QColor

#* ------------------------------------------------------------ *#

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# * ------------------------------------------------------------ *#

from SD4LE_config import SD4LEConfig

from src.img.img import *

from etc.dpi_getter import get_dpi, dpi_to_percent

#* ------------------------------------------------------------ *#


class StyleSheets(Enum): 
    window = """
        QMainWindow{
            background: url(:/img/background.jpg);
            background-repeat: no-repeat;
            background-position: center;
        }
    """

    body_frame = """
        QFrame{
            background: rgba(255, 255, 255, 135);
            border: 1px solid #ffffff;
        }
    """

    bold_text = """
        QLabel{
            border: none;
            background: none;
            color: #333333;
        }
    """

    regular_text = """
        QLabel{
            border: none;
            background: none;
            color: #555555;
        }
    """

    stick_text = """
        QLabel{
            border: none;
            background: none;
            color: #8a8a8a;
        }
    """

    login_frame = """
        QFrame{
            background: #ffffff;
            border-top: 1px solid #000000;
        }
    """

    login_text = """
        QLabel{
            border: none;
            color: #114c6c;
        }
    """

    account_frame = """
        QFrame{
            border: 1px solid #dddddd;
        }
    """

    account_title = """
        QLabel{
            background: url(:/img/login_title.png);
            background-repeat: no-repeat;
            background-position: center;

            border: 0px;
        }
    """

    account_info = """
        QLabel{
            border: 1px solid #eaeaea;
            color: #333333;
        }
    """

    account_text = """
        QLabel{
            border: none;
            color: #555555;
        }
    """

    account_box = """
        QLineEdit{
            border: 1px solid #bbbbbb;
            background: #fcfcfc;
        }
    """

    login_button = """
        QPushButton{
            background: none;
            border: none;
            background-color: #1e9d44;
            color: #ffffff;
        }
    """
    
    # --- End of StyleSheets --- #




class MainUI(QMainWindow): 
    def __init__(self) -> None: 
        super().__init__()

        self.dpi_percent = dpi_to_percent(get_dpi())

        self.mainUI()
        self.signal()

        # --- End of __init__() --- #



    def mainUI(self) -> None: 
        # Basic part
        self.setFixedSize(1061, 663)
        self.setWindowTitle("SD4LE")
        icon_path = SD4LEConfig.ICON_PATH
        if os.path.isfile(icon_path): 
            self.setWindowIcon(QIcon(icon_path))
        font_path = SD4LEConfig.FONT_PATH
        if os.path.isfile(font_path): 
            QFontDatabase.addApplicationFont(font_path)
        

        # Window part
        self.setStyleSheet(StyleSheets.window.value)


        # Body part
        self.body_FRM = QFrame(self)
        self.body_FRM.setGeometry(70, 30, 921, 603)
        self.body_FRM.setStyleSheet(StyleSheets.body_frame.value)

        self.howToUse1_LB = QLabel(self.body_FRM)
        if self.dpi_percent <= 100: 
            self.howToUse1_LB.setGeometry(40, 34, 122, 34)
        else: 
            self.howToUse1_LB.setGeometry(40, 34, 143, 37)
        self.howToUse1_LB.setFont(QFont("나눔고딕OTF", 23, QFont.Weight.Bold))
        self.howToUse1_LB.setStyleSheet(StyleSheets.bold_text.value)
        self.howToUse1_LB.setText("이용안내")

        self.howToUse2_LB = QLabel(self.body_FRM)
        if self.dpi_percent <= 100: 
            self.howToUse2_LB.setGeometry(168, 34, 10, 34)
        else: 
            self.howToUse2_LB.setGeometry(190, 34, 10, 34)
        self.howToUse2_LB.setFont(QFont("나눔고딕OTF", 23))
        self.howToUse2_LB.setStyleSheet(StyleSheets.stick_text.value)
        self.howToUse2_LB.setText("|")

        self.howToUse3_LB = QLabel(self.body_FRM)
        if self.dpi_percent <= 100: 
            self.howToUse3_LB.setGeometry(186, 35, 470, 30)
            self.howToUse3_LB.setFont(QFont("굴림체", 10))
        else: 
            self.howToUse3_LB.setGeometry(208, 35, 500, 33)
            self.howToUse3_LB.setFont(QFont("굴림체", 9))
        self.howToUse3_LB.setStyleSheet(StyleSheets.regular_text.value)
        self.howToUse3_LB.setText("교내 연구실 안전교육을 자동으로 진행 및 완료하는 프로그램입니다.\n본 프로그램 사용의 책임은 사용자에게 있습니다.")


        # Login part
        self.login_FRM = QFrame(self.body_FRM)
        self.login_FRM.setGeometry(40, 93, 841, 457)
        self.login_FRM.setStyleSheet(StyleSheets.login_frame.value)

        self.login_LB = QLabel(self.login_FRM)
        if self.dpi_percent <= 100: 
            self.login_LB.setGeometry(30, 31, 100, 37)
            self.login_LB.setFont(QFont("나눔고딕OTF", 26, QFont.Weight.Bold))
        else: 
            self.login_LB.setGeometry(30, 31, 116, 41)
            self.login_LB.setFont(QFont("나눔고딕OTF", 25, QFont.Weight.Bold))
        self.login_LB.setStyleSheet(StyleSheets.login_text.value)
        self.login_LB.setText("로그인")

        self.account_FRM = QFrame(self.login_FRM)
        self.account_FRM.setGeometry(188, 93, 465, 353)
        self.account_FRM.setStyleSheet(StyleSheets.account_frame.value)

        self.accountTitle_LB = QLabel(self.account_FRM)
        self.accountTitle_LB.setGeometry(-1, 0, 467, 60)
        self.accountTitle_LB.setStyleSheet(StyleSheets.account_title.value)

        self.accountInfo_LB = QLabel(self.account_FRM)
        if self.dpi_percent <= 100: 
            self.accountInfo_LB.setGeometry(41, 81, 385, 35)
            self.accountInfo_LB.setFont(QFont("굴림체", 10, QFont.Weight.Bold))
        else: 
            self.accountInfo_LB.setGeometry(40, 81, 385, 35)
            self.accountInfo_LB.setFont(QFont("굴림체", 11, QFont.Weight.Bold))
        self.accountInfo_LB.setStyleSheet(StyleSheets.account_info.value)
        self.accountInfo_LB.setText("학생/교원/직원 로그인")
        self.accountInfo_LB.setAlignment(Qt.AlignCenter)

        self.userID_LB = QLabel(self.account_FRM)
        if self.dpi_percent <= 100: 
            self.userID_LB.setGeometry(103, 139, 45, 18)
            self.userID_LB.setFont(QFont("굴림체", 10, QFont.Weight.Bold))
        else: 
            self.userID_LB.setGeometry(93, 139, 55, 19)
            self.userID_LB.setFont(QFont("굴림체", 11, QFont.Weight.Bold))
        self.userID_LB.setStyleSheet(StyleSheets.account_text.value)
        self.userID_LB.setText("아이디")

        self.userID_LE = QLineEdit(self.account_FRM)
        if self.dpi_percent <= 100: 
            self.userID_LE.setGeometry(155, 136, 234, 27)
            self.userID_LE.setFont(QFont("굴림체", 9))
        else: 
            self.userID_LE.setGeometry(155, 136, 236, 28)
            self.userID_LE.setFont(QFont("굴림체", 10))
        self.userID_LE.setStyleSheet(StyleSheets.account_box.value)
        
        self.userPW_LB = QLabel(self.account_FRM)
        if self.dpi_percent <= 100: 
            self.userPW_LB.setGeometry(88, 176, 60, 14)
            self.userPW_LB.setFont(QFont("굴림체", 10, QFont.Weight.Bold))
        else: 
            self.userPW_LB.setGeometry(73, 176, 75, 19)
            self.userPW_LB.setFont(QFont("굴림체", 11, QFont.Weight.Bold))
        self.userPW_LB.setStyleSheet(StyleSheets.account_text.value)
        self.userPW_LB.setText("비밀번호")

        self.userPW_LE = QLineEdit(self.account_FRM)
        if self.dpi_percent <= 100: 
            self.userPW_LE.setGeometry(155, 171, 234, 27)
            self.userPW_LE.setFont(QFont("굴림체", 9))
        else: 
            self.userPW_LE.setGeometry(155, 171, 236, 28)
            self.userPW_LE.setFont(QFont("굴림체", 10))
        self.userPW_LE.setStyleSheet(StyleSheets.account_box.value)
        self.userPW_LE.setEchoMode(QLineEdit.Password)

        self.login_BT = QPushButton(self.account_FRM)
        if self.dpi_percent <= 100: 
            self.login_BT.setGeometry(159, 231, 150, 33)
            self.login_BT.setFont(QFont("나눔고딕OTF", 11, QFont.Weight.Bold))
        else: 
            self.login_BT.setGeometry(152, 231, 161, 39)
            self.login_BT.setFont(QFont("나눔고딕OTF", 12, QFont.Weight.Bold))
        self.login_BT.setStyleSheet(StyleSheets.login_button.value)
        self.login_BT.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.login_BT.setText("로그인")
        self.login_BT.setCursor(Qt.PointingHandCursor)

        self.inquiry1_LB = QLabel(self.body_FRM)
        if self.dpi_percent <= 100: 
            self.inquiry1_LB.setGeometry(41, 577, 61, 18)
            self.inquiry1_LB.setFont(QFont("굴림체", 10, QFont.Weight.Bold))
        else: 
            self.inquiry1_LB.setGeometry(41, 577, 73, 18)
            self.inquiry1_LB.setFont(QFont("굴림체", 11, QFont.Weight.Bold))
        self.inquiry1_LB.setStyleSheet(StyleSheets.bold_text.value)
        self.inquiry1_LB.setText("이용문의")
        
        self.inquiry2_LB = QLabel(self.body_FRM)
        if self.dpi_percent <= 100: 
            self.inquiry2_LB.setGeometry(112, 577, 7, 18)
            self.inquiry2_LB.setFont(QFont("나눔고딕OTF", 10))
        else: 
            self.inquiry2_LB.setGeometry(126, 577, 7, 18)
            self.inquiry2_LB.setFont(QFont("나눔고딕OTF", 11, QFont.Weight.Bold))
        self.inquiry2_LB.setStyleSheet(StyleSheets.stick_text.value)
        self.inquiry2_LB.setText("|")

        self.inquiry3_LB = QLabel(self.body_FRM)
        if self.dpi_percent <= 100: 
            self.inquiry3_LB.setGeometry(126, 577, 750, 18)
            self.inquiry3_LB.setFont(QFont("굴림체", 10))
        else: 
            self.inquiry3_LB.setGeometry(140, 577, 720, 18)
            self.inquiry3_LB.setFont(QFont("굴림체", 11))
        self.inquiry3_LB.setStyleSheet(StyleSheets.regular_text.value)
        self.inquiry3_LB.setText("개발자에게 문의")
        
        # --- End of mainUI() --- #



    def signal(self) -> None: 
        pass                # Test code / please delete this line.
        
        # --- End of signal() --- #
    
    ## --- End of MainUI() --- ##





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

    mainUI = MainUI()
    mainUI.show()
    sys.exit(app.exec())
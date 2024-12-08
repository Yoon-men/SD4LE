import sys
import os

from PySide6.QtCore import QObject, Signal

import traceback

from typing import Optional

# * ------------------------------------------------------------ *#

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# * ------------------------------------------------------------ *#

from SD4LE_config import SD4LEConfig

from etc.driver_manager import DriverManager

from func.sandevistan import Sandevistan

#* ------------------------------------------------------------ *#


class Operation(QObject):
    show_loading_window_signal = Signal()
    open_alert_window_signal = Signal(str)

    def run(self, id: str, pw: str) -> None:
        self.show_loading_window_signal.emit()
        
        self.id: str = id
        self.pw: str = pw
        if not self.is_login_input_valid(self.id, self.pw):
            self.open_alert_window_signal.emit("ID, PW가 모두 입력되었는지\n확인해 주세요.")
            SD4LEConfig.logger.warning("STOP: 산데비스탄 가동 중지 (login_input_is_not_valid)")
            return
        
        self.DB_manager = SD4LEConfig.DB_manager
        if not self.is_user_allowed(self.id):
            self.open_alert_window_signal.emit(self.DB_manager.get_unwelcome_message())
            SD4LEConfig.logger.warning("STOP: 산데비스탄 가동 중지 (user_is_not_allowed)")
            return

        self.success: bool = False
        self.error_message: Optional[str] = None


        driver_flag: bool = False
        try:
            self.driver_manager = DriverManager()
            driver_flag = True
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(
                exc_type, exc_value, exc_traceback
            )
            self.error_message = "".join(formatted_traceback)
            self.open_alert_window_signal.emit("Chrome, Edge, Firefox 브라우저를\n모두 찾을 수 없어\nWebDriver를 생성할 수 없습니다.")

        if driver_flag:
            try:
                self.driver_manager = DriverManager()
                self.sandevistan = Sandevistan(driver=self.driver_manager.driver, id=self.id, pw=self.pw)

                self.error_message: Optional[str] = self.operate()
                self.success = True if not self.error_message else False
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                formatted_traceback = traceback.format_exception(
                    exc_type, exc_value, exc_traceback
                )
                self.error_message = "".join(formatted_traceback)


        self.DB_manager.add_execution_history(
            user_id=self.id, 
            success=self.success, 
            error_message=self.error_message
        )

        if self.success:
            SD4LEConfig.DB_manager.add_user(
                user_id=self.id
            )

        return



    def is_login_input_valid(self, ID: str, PW: str) -> bool:
        return False if (ID == '') or (PW == '') else True
    


    def is_user_allowed(self, user_id: str) -> bool:
        try:
            # Step 1: 'allow_non_whitelisted_users' 값을 확인
            allow_non_whitelisted = self.DB_manager.get_allow_non_whitelisted_users()
            if allow_non_whitelisted:
                return True
            else:
                # Step 2: 'users' 테이블에서 해당 'user_id'의 'is_whitelisted' 값을 확인
                response = self.DB_manager.supabase.table('users')\
                    .select('is_whitelisted')\
                    .eq('user_id', user_id)\
                    .single()\
                    .execute()
                if response.data and response.data.get('is_whitelisted'):
                    return response.data['is_whitelisted']
                else:
                    return False
        except Exception as e:
            # # 오류 발생 시 False 반환 및 로그 기록
            # exc_type, exc_value, exc_traceback = sys.exc_info()
            # formatted_traceback = traceback.format_exception(
            #     exc_type, exc_value, exc_traceback
            # )
            # exc_msg = "".join(formatted_traceback)
            # SD4LEConfig.logger.error(f"Error occurred while checking access for user '{user_id}':\n{exc_msg}")
            return False



    def operate(self) -> Optional[str]:
        SD4LEConfig.logger.info("START: 산데비스탄 가동")
        
        cheap_but_similar = {
            "this_fffire"                        : "STOP : 산데비스탄 가동 중지 (this_fffire)",
            "whos_ready_for_tomorrow"            : "STOP : 산데비스탄 가동 중지 (whos_ready_for_tomorrow)",
            "friday_night_fire_fight"            : "STOP : 산데비스탄 가동 중지 (friday_night_fire_fight)",
            "i_really_want_to_stay_at_your_house": "STOP : 산데비스탄 가동 중지 (i_really_want_to_stay_at_your_house)",
            "let_you_down"                       : "STOP : 산데비스탄 가동 중지 (let_you_down)"
        }

        for function, log in cheap_but_similar.items():
            error_message: Optional[str] = getattr(self.sandevistan, function)()
            if error_message:
                alert_txt = "잘못된 계정 정보입니다.\nID와 PW를 다시 확인해 주세요." \
                            if function == "whos_ready_for_tomorrow" \
                            else \
                            "에러가 발생했습니다.\n개발자에게 로그 파일과 함께\n문의해 주세요."
                self.open_alert_window_signal.emit(alert_txt)
                SD4LEConfig.logger.error(log)
                return error_message
        
        self.open_alert_window_signal.emit("작업을 완료했습니다.")
        SD4LEConfig.logger.info("E N D: 산데비스탄 완료")
        return None
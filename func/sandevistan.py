import sys
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementNotInteractableException,
    JavascriptException,
    NoAlertPresentException,
)

import time
import openai
import traceback
from typing import Optional

import requests

# * ------------------------------------------------------------ *#

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# * ------------------------------------------------------------ *#

from SD4LE_config import SD4LEConfig

from etc.driver_manager import DriverManager

#* ------------------------------------------------------------ *#


class Sandevistan(): 
    driver: Optional[webdriver.Chrome | webdriver.Edge | webdriver.Firefox] = None

    def __init__(self, driver, id, pw): 
        self.driver = driver

        self.id = id
        self.pw = pw

        self.max_sbj = -1

        # --- End of __init__() --- #



    def this_fffire(self) -> Optional[str]: 
        """
        This func allows the driver to access to the site.
        """
        try: 
            self.driver.get("https://labsafety.kumoh.ac.kr/")
            self.driver.find_element(By.XPATH, '//*[@id="contents"]/div[1]/div[3]/a').click()
            return None
        except: 
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
            SD4LEConfig.logger.error(f"An error occurred in the this_fffire.\n{''.join(formatted_traceback)}")

            self.driver.close()
            return ''.join(formatted_traceback)
        
        # --- End of this_fffire() --- #
    

    def whos_ready_for_tomorrow(self) -> Optional[str]: 
        """
        This func allows the driver to login.
        """
        try: 
            self.driver.find_element(By.XPATH, '//*[@id="stdUniqueKey"]').send_keys(self.id)
            self.driver.find_element(By.XPATH, '//*[@id="stdPassword"]').send_keys(self.pw)

            self.driver.find_element(By.XPATH, '//*[@id="btnStudent"]').click()

            try: 
                self.driver.switch_to.alert.accept()
                self.driver.close()
                return "잘못된 계정 정보입니다.\nID와 PW를 다시 확인해 주세요."
            except NoAlertPresentException: 
                return None
        except: 
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
            SD4LEConfig.logger.error(f"An error occurred in the whos_ready_for_tomorrow.\n{''.join(formatted_traceback)}")

            self.driver.close()
            return ''.join(formatted_traceback)
        
        # --- End of whos_ready_for_tomorrow() --- #


    def friday_night_fire_fight(self) -> Optional[str]: 
        """
        This func allows the driver to select subjects
        """
        try: 
            try: 
                self.driver.find_element(By.XPATH, '//*[@id="btnMappingContent"]/img').click()

                crt_sbj, self.max_sbj = map(int, self.driver.find_element(By.XPATH, '//*[@id="MappingContent_spSelectCount"]').text.split(' / '))
                for i in range(crt_sbj+1, self.max_sbj+1) : 
                    self.driver.find_element(By.XPATH, f'//*[@id="MappingContent_tblList"]/tbody/tr[{i}]/td[1]/input[2]').click()
                
                self.driver.find_element(By.XPATH, '//*[@id="MappingContent_btnSave"]').click()
                return None
            except ElementNotInteractableException: 
                self.max_sbj = 2
                while True : 
                    if not self.driver.find_elements(By.XPATH, f'//*[@id="divProgressInfList"]/table/tbody/tr[{self.max_sbj}]/td[7]/input') : break
                    self.max_sbj += 1
                self.max_sbj -= 2
                return None
        except: 
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
            SD4LEConfig.logger.error(f"An error occurred in the friday_night_fire_fight.\n{''.join(formatted_traceback)}")
            
            self.driver.close()
            return ''.join(formatted_traceback)

        # --- End of friday_night_fire_fight() --- #
    

    def i_really_want_to_stay_at_your_house(self) -> Optional[str]: 
        """
        This func allows the driver to skip lectures.
        """
        try: 
            for i in range(2, 2+self.max_sbj) : 
                self.driver.find_element(By.XPATH, f'//*[@id="divProgressInfList"]/table/tbody/tr[{i}]/td[7]/input').click()
                self.driver.switch_to.window(self.driver.window_handles[-1])
                time.sleep(1)
                try : 
                    self.driver.execute_script("opener.PageMove2019AfterVersion(totalPageNum);")
                except JavascriptException : 
                    self.driver.execute_script("opener.PageMove2019AfterVersion(chapterInfo.length);")
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
            return None
        except: 
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
            SD4LEConfig.logger.error(f"An error occurred in the i_really_want_to_stay_at_your_house.\n{''.join(formatted_traceback)}")
            
            self.driver.close()
            return ''.join(formatted_traceback)

        # --- End of i_really_want_to_stay_at_your_house() --- #


    def let_you_down(self) -> Optional[str]: 
        """
        This func allows the driver to solve quizs.
        """
        try: 
            self.driver.find_element(By.XPATH, '//*[@id="ProgressInfoList_btnExam"]').click()

            openai.api_key = SD4LEConfig.DB_manager.get_api_key()
            time.sleep(0.5)
            exam_question = self.driver.find_element(By.ID, "frmExam").text.encode("utf-8").decode("utf-8")
            SD4LEConfig.logger.debug(f"\nexam_question: {exam_question}")               # Test code / please delete this line.

            def oh_let_you_down(answer_text: str) -> bool: 
                """
                This func allows the driver to find and click the answer.
                """
                labels = self.driver.find_elements(By.TAG_NAME, "label")
                for label in labels : 
                    if (answer_text == label.text) and (label not in clicked_labels_set) : 
                        label.click()
                        time.sleep(0.5)
                        clicked_labels_set.add(label)
                        return True
                SD4LEConfig.logger.debug(f"'{answer_text}'를 갖는 label을 찾을 수 없었습니다.")              # Test code / please delete this line.
                return False                # answer_text를 갖는 label을 찾을 수 없는 경우
            
                # --- End of oh_let_you_down() --- #

            while True: 
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You're a safety manager. When presented with a question, print the answer to the question in Python dict format (key is the question number and value is the answer(ONLY STR!) to the question)."},
                        {"role": "user", "content": exam_question}
                    ]
                )

                SD4LEConfig.logger.debug(f"\noriginal answers: {response.choices[0].message.content}")               # Test code / please delete this line.

                ## Feel the rhythm of the streets
                gptSaid = response.choices[0].message.content
                try: 
                    answers = eval(gptSaid)
                except SyntaxError: 
                    gptSaid = gptSaid.lstrip("```python").rstrip("```")
                    answers = eval(gptSaid)

                ## Neon lights and neon dreams
                if len(answers) < 10: 
                    continue

                SD4LEConfig.logger.debug(f"\npolished answers: {answers}")               # Test code/  please delete this line.
                if not isinstance(answers, dict) : continue

                clicked_labels_set = set()
                if all(oh_let_you_down(answer_text) for answer_text in answers.values()) : 
                    SD4LEConfig.logger.info("문제를 모두 풀었습니다.")                # Test code / please delte this line.
                    break
                else: 
                    continue

            self.driver.find_element(By.XPATH, '//*[@id="Exam_btnSave"]').click()
            time.sleep(0.5)
            SD4LEConfig.logger.info("제출 완료")
            alert = self.driver.switch_to.alert
            if ("모든 문제를" in alert.text) or ("재평가" in alert.text): 
                alert.accept()
                self.let_you_down()
            else: 
                alert.accept()
                self.driver.close()
                return None
        except: 
            exc_type, exc_value, exc_traceback = sys.exc_info()
            formatted_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
            SD4LEConfig.logger.error(f"An error occurred in the let_you_down.\n{''.join(formatted_traceback)}")

            self.driver.close()
            return ''.join(formatted_traceback)

            # --- End of major_crimes() --- #
        
        # --- End of let_you_down() --- #


if __name__ == "__main__": 
    user_id = "20771234"
    user_pw = "wa!sans!"
    driver_manager = DriverManager()
    sandevistan = Sandevistan(driver=driver_manager.driver, id=user_id, pw=user_pw)

    sandevistan.this_fffire()
    sandevistan.whos_ready_for_tomorrow()
    sandevistan.friday_night_fire_fight()
    sandevistan.i_really_want_to_stay_at_your_house()
    sandevistan.let_you_down()
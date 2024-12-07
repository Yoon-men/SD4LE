"""
Driver-Manager

ver 1.1.0

~ 15:18 on Sat, Dec 7, 2024 ~
"""

# * ------------------------------------------------------------ *#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.options import Options as SafariOptions

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from selenium.common.exceptions import WebDriverException

from typing import Optional

# * ------------------------------------------------------------ *#


class DriverManager:
    driver: Optional[webdriver.Chrome | webdriver.Edge | webdriver.Firefox | webdriver.Safari] = None


    def __init__(self) -> None:
        for make_driver in [
            self.make_chrome_driver,
            self.make_edge_driver,
            self.make_firefox_driver
            # self.make_safari_driver
        ]:
            try: 
                self.driver = make_driver()
                return
            except: 
                continue
        
        raise WebDriverException("Chrome, Edge, Firefox 브라우저를 모두 찾을 수 없어 WebDriver를 생성할 수 없습니다.")



    def make_chrome_driver(self) -> webdriver.Chrome:
        options = ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option(
            "excludeSwitches", ["enable-logging", "enable-automation"]
        )
        options.add_experimental_option("detach", True)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--mute-audio")

        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        driver.implicitly_wait(2)

        return driver



    def make_edge_driver(self) -> webdriver.Edge:
        options = EdgeOptions()
        options.add_argument("start-maximized")
        options.detach = True
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--mute-audio")
        
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
        driver.implicitly_wait(2)

        return driver



    def make_firefox_driver(self) -> webdriver.Firefox:
        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--mute-audio")
        
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
        driver.implicitly_wait(2)
        
        return driver



    def make_safari_driver(self) -> webdriver.Safari:
        options = SafariOptions()

        driver = webdriver.Safari(options=options)
        driver.implicitly_wait(2)

        return driver
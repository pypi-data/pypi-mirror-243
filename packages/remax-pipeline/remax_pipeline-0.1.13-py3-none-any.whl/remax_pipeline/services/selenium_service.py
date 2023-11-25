from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    op = webdriver.ChromeOptions()
    op.add_argument("--headless")

    service = Service(executable_path=ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=op)
    return driver


class HTMLStackParser:
    def __init__(self):
        pass

    @classmethod
    def parse_web_element(self, element):
        html = element.get_attribute("outerHTML")

        innerText = []
        text = ""

        for i in html:
            if i == ">":
                text = ""
            elif i == "<":
                if text != "":
                    innerText.append(text)
            else:
                text = text + i
        return innerText

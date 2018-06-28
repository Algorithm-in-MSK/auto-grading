import time
from urllib.error import URLError

import docker
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys

from results import BOJ_RESULT

CHROME = DesiredCapabilities.CHROME.copy()
REMOTE_URI = "http://selenium:4444/wd/hub"
DRIVER = None


# def run_selenium_container():
#     client = docker.from_env()


def set_driver():
    print("Waiting for selenium driver...")
    while True:
        try:
            _driver = webdriver.Remote(desired_capabilities=DesiredCapabilities.CHROME, command_executor=REMOTE_URI)
            break
        except URLError:
            time.sleep(0.1)
    return _driver


def get_message():
    from selector import RESULT_MSG
    try:
        return DRIVER.find_element_by_css_selector(RESULT_MSG).text.strip()
    except Exception:
        return None


def get_result():
    print("Getting result...")
    prev = None
    while True:
        msg = get_message()
        if prev != msg and msg is not None:
            print(msg)
            prev = msg
        if msg in BOJ_RESULT.keys():
            print(BOJ_RESULT[msg])
            break


def login():
    print("Trying login...")
    from selector import ID, PASSWORD, LOGIN
    from credential import USER_ID, USER_PASSWORD

    DRIVER.get("https://www.acmicpc.net/login")
    DRIVER.find_element_by_css_selector(ID).send_keys(USER_ID)
    DRIVER.find_element_by_css_selector(PASSWORD).send_keys(USER_PASSWORD)
    DRIVER.find_element_by_css_selector(LOGIN).click()


def submit():
    from selector import CODE_SUBMIT
    print("Submitting code...")
    DRIVER.get("https://www.acmicpc.net/submit/2011")
    select_language()
    type_code()
    DRIVER.find_element_by_css_selector(CODE_SUBMIT).click()


def _delete_all_left_white_spaces():
    webdriver.ActionChains(DRIVER).key_down(Keys.CONTROL).key_down(Keys.SHIFT).send_keys(Keys.LEFT).key_up(
        Keys.CONTROL).key_up(Keys.SHIFT).perform()


def type_code():
    print("Typing code...")
    e = DRIVER.switch_to.active_element
    with open("sean/2011.py", 'r') as sf:
        code = sf.readlines()
        for c in code:
            _delete_all_left_white_spaces()
            e.send_keys(Keys.DELETE)
            e.send_keys(c)
            e.send_keys(Keys.ENTER)


def select_language(language="Python3"):
    from selector import LANGUAGE_DROPDOWN, LANGUAGE_SELECT, CODE_SUBMIT
    print("Selecting language...")
    DRIVER.find_element_by_css_selector(LANGUAGE_DROPDOWN).click()
    DRIVER.find_element_by_css_selector(LANGUAGE_SELECT).click()
    DRIVER.find_element_by_css_selector(CODE_SUBMIT).click()
    print("Select language with ", language)


if __name__ == "__main__":
    DRIVER = set_driver()
    assert DRIVER is not None

    login()
    submit()
    get_result()

    DRIVER.close()

import json
import os
import pathlib
import platform
import time
import mintotp

import core.common.commoncomponent as self
from core.common.constants import instruction_operations
from core.common.models import login_credentails_dto
from core.common.repository import data_platorm
from core.common.repository import dp_applicant_login_info
from core.common.repository import login_path
from core.common.utils import gmail_login as login
from core.seleniumcore.pagefactory import seleniumcommon
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


element_wait_timeout = 10

def add_drivers_to_path():
    path_constant = 'PATH'
    print("Adding webdrivers to path.")
    curr_file_path = pathlib.Path(__file__).parent.absolute()
    if platform.system() == 'Darwin':
        webdriver_path = os.path.join(curr_file_path, 'webdrivers', 'mac')
    elif platform.system() == 'Windows':
        webdriver_path = os.path.join(curr_file_path, 'webdrivers', 'windows')
    elif platform.system() == 'Linux':
        webdriver_path = os.path.join(curr_file_path, 'webdrivers', 'linux')
    else:
        raise Exception("Unknown platform. Unable to add webdrivers to path.")
    current_path = os.environ[path_constant]
    new_path = webdriver_path + ':' + current_path
    os.environ[path_constant] = new_path


def login_to_application(data_platform_name, username, password):
    login_credentails_dto.username = username
    login_credentails_dto.password = password
    global data_platform_id
    data_platform_id = data_platorm.fetch_dataplatform_id(data_platform_name)
    login_credentails_dto.data_platform_id = data_platform_id
    # always start from level 1
    login_instructions = login_path.fetch_login_path_instructions(data_platform_id, 1)
    instructions_to_perform(login_instructions)


def instructions_to_perform(login_instructions):
    global login_instruction
    for login_instruction in login_instructions:
        getattr(self, instruction_operations.options[login_instruction['op_name']])()


def navigate_url():
    global driver
    global url
    add_drivers_to_path()
    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-popup-blocking")
    # chrome_options.add_argument("--profile-directory=Default")
    # chrome_options.add_argument("--ignore-certificate-errors")
    # chrome_options.add_argument("--disable-plugins-discovery")
    # #chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--lang=en-us")
    # chrome_options.add_argument("--disable-web-security")
    # chrome_options.add_argument("--allow-running-insecure-content")
    # chrome_options.add_argument("user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0'")
    # chrome_options.add_argument("start-maximized")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument("--remote-debugging-port=9222")
    # chrome_options.add_argument("--disable-web-security")
    # chrome_options.add_argument("--allow-running-insecure-content")
    # chrome_options.add_argument("--enable-experimental-cookie-features")
    #chrome_options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])

    # chrome_options.add_experimental_option("prefs", {"profile.block_third_party_cookies": False});
    # ua = UserAgent()
    # userAgent = ua.random
    # print(userAgent)
    # chrome_options.add_argument(f'user-agent={userAgent}')
    # chrome_options.add_experimental_option("excludeSwitches",
    #                                 ["ignore-certificate-errors", "safebrowsing-disable-download-protection",
    #                                  "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
    # driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    #     "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'})
    # print(driver.execute_script("return navigator.userAgent;"))
    driver = webdriver.Chrome()
    #driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    if login_instruction['element_key_name'] == 'mfa-url' or login_instruction['element_key_name'] == 're-login-url':
        driver.execute_cdp_cmd('Network.enable', {})
        for cookie in otpcookies:
            driver.execute_cdp_cmd('Network.setCookie', cookie)
        driver.execute_cdp_cmd('Network.disable', {})
    else:
        url = login_instruction['element_key_value']
    print("Navigating to URL: {}".format(url))
    driver.get(url);


def verify():
    pagetovalidate = login_instruction['element_identifier'].split('=', 1)
    WebDriverWait(driver, element_wait_timeout).until(EC.presence_of_element_located((pagetovalidate[0], pagetovalidate[1])))
    return "Varifying page complete"


def fill():
    type_and_value = login_instruction['element_identifier'].split('=', 1)
    if (login_instruction['element_key_value'] is None):
        if (login_instruction['element_key_name'] == 'username'):
            WebDriverWait(driver, element_wait_timeout).until(
                EC.element_to_be_clickable((type_and_value[0], type_and_value[1])))
            seleniumcommon.type_into_element(driver, login_credentails_dto.username,
                                             type_and_value[0], type_and_value[1])
            dp_applicant_login_info.update_username(login_credentails_dto.username, data_platform_id)
        if (login_instruction['element_key_name'] == 'password'):
            WebDriverWait(driver, element_wait_timeout).until(
                EC.element_to_be_clickable((type_and_value[0], type_and_value[1])))
            seleniumcommon.type_into_element(driver, login_credentails_dto.password,
                                             type_and_value[0], type_and_value[1])
            dp_applicant_login_info.update_password(login_credentails_dto.password, data_platform_id)
    else:
        seleniumcommon.type_into_element(driver, login_instruction['element_key_value'],
                                         type_and_value[0], type_and_value[1])


def click():
    type_and_value = login_instruction['element_identifier'].split('=', 1)
    seleniumcommon.click(driver, type_and_value[0], type_and_value[1])


def check():
    type_and_value = login_instruction['element_identifier'].split('=', 1)
    WebDriverWait(driver, element_wait_timeout).until(
        EC.presence_of_element_located((type_and_value[0], type_and_value[1])))
    if seleniumcommon.assert_radio_is_selected(driver, type_and_value[0], type_and_value[1]) == False:
        seleniumcommon.click(driver, type_and_value[0], type_and_value[1])


def close_window():
    seleniumcommon.stopdriver(driver)


def save_mfa_session():
    url = driver.current_url
    print("Current to URL: {}".format(url))
    otpcookies = driver.get_cookies()
    dp_applicant_login_info.update_mfa_cookies(url, data_platform_id)
    login_credentails_dto.temp_currenturl=url
    login_credentails_dto.temp_otpcookies=otpcookies


def save_login_session():
    url = driver.current_url
    print("Current to URL: {}".format(url))
    otpcookies = driver.get_cookies()
    dp_applicant_login_info.update_login_cookies(url, data_platform_id)


def verify_and_fork():
    jsonvalue = json.loads(login_instruction['element_identifier'])
    for key, value in jsonvalue.items():
        pagetovalidate = key.split('=', 1)
        time.sleep(5)
        if (seleniumcommon.is_element_visible(driver, pagetovalidate[0], pagetovalidate[1])):
            sequences = login_path.fetch_login_path_sequence(data_platform_id, value)
            sequence_to_perform(sequences)
        else:
            print("not able to find page, looking for another page")

def gmail_login():
    login_credentails_dto.driver = driver
    handles = driver.window_handles
    size = len(handles)
    parent_handle = driver.current_window_handle
    for x in range(size):
        if handles[x] != parent_handle:
            driver.switch_to.window(handles[x])
            result = login.enter_username_password(login_credentails_dto.username, login_credentails_dto.password)
            if result == True:
                login.enter_otp(mintotp.totp('6wtgspfm3uls3nrrdz7ssmqcsuqldwu2'))
            time.sleep(7)
            driver.quit()
            break

    driver.switch_to.window(parent_handle)


def operation_completed():
    print("All operation completed => Enjoy")

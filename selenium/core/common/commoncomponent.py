import json
import os
import pathlib
import platform
import time

import core.common.commoncomponent as self
from core.common.constants import login_operations
from core.common.models import login_credentails_dto
from core.common.repository import data_platorm
from core.common.repository import dp_applicant_login_info
from core.common.repository import login_path
from core.common.utils import gmail_login as login
from core.seleniumcore.pagefactory import seleniumcommon
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def add_drivers_to_path():
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
    current_path = os.environ['PATH']
    new_path = webdriver_path + ':' + current_path
    os.environ['PATH'] = new_path


def login_to_application(applicationname, username, password):
    login_credentails_dto.username = username
    login_credentails_dto.password = password
    global data_platform_id
    data_platform_id = data_platorm.fetch_dataplatform_id(applicationname)
    sequences = login_path.fetch_login_path_sequence(data_platform_id, 1)
    sequence_to_perform(sequences)


def sequence_to_perform(sequences):
    global operation
    for operation in sequences:
        getattr(self, login_operations.options[operation['op_name']])()


def navigate_url():
    global driver
    global url
    add_drivers_to_path()
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    if operation['element_key_name'] == 'mfa-url' or operation['element_key_name'] == 're-login-url':
        driver.execute_cdp_cmd('Network.enable', {})
        for cookie in otpcookies:
            driver.execute_cdp_cmd('Network.setCookie', cookie)
        driver.execute_cdp_cmd('Network.disable', {})
    else:
        url = operation['element_key_value']
    print("Navigating to URL: {}".format(url))
    driver.get(url);


def verify():
    pagetovalidate = operation['element_identifier'].split('=', 1)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((pagetovalidate[0], pagetovalidate[1])))
    return "Varifying page complete"


def fill():
    type_and_value = operation['element_identifier'].split('=', 1)
    if (operation['element_key_value'] is None):
        if (operation['element_key_name'] == 'username'):
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((type_and_value[0], type_and_value[1])))
            seleniumcommon.type_into_element(driver, login_credentails_dto.username,
                                             type_and_value[0], type_and_value[1])
            dp_applicant_login_info.update_username(login_credentails_dto.username, data_platform_id)
        if (operation['element_key_name'] == 'password'):
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((type_and_value[0], type_and_value[1])))
            seleniumcommon.type_into_element(driver, login_credentails_dto.password,
                                             type_and_value[0], type_and_value[1])
            dp_applicant_login_info.update_password(login_credentails_dto.password, data_platform_id)
    else:
        seleniumcommon.type_into_element(driver, operation['element_key_value'],
                                         type_and_value[0], type_and_value[1])


def click():
    type_and_value = operation['element_identifier'].split('=', 1)
    seleniumcommon.click(driver, type_and_value[0], type_and_value[1])


def check():
    type_and_value = operation['element_identifier'].split('=', 1)
    WebDriverWait(driver, 10).until(
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


def save_login_session():
    url = driver.current_url
    print("Current to URL: {}".format(url))
    otpcookies = driver.get_cookies()
    dp_applicant_login_info.update_login_cookies(url, data_platform_id)


def verify_and_fork():
    jsonvalue = json.loads(operation['element_identifier'])
    for key, value in jsonvalue.items():
        pagetovalidate = key.split('=', 1)
        try:
            time.sleep(1)
            if (seleniumcommon.is_element_visible(driver, pagetovalidate[0], pagetovalidate[1])):
                sequences = login_path.fetch_login_path_sequence(data_platform_id, value)
                break
        except:
            print("not able to find page, looking for another page")
    sequence_to_perform(sequences)


def gmail_login():
    login_credentails_dto.driver = driver
    parent_handle = driver.current_window_handle
    seleniumcommon.handle_window(driver, parent_handle)
    result = login.enter_username_password(login_credentails_dto.username, login_credentails_dto.password)
    if result == True:
        login.enter_otp(mintotp.totp('js6aegv5sm5mqw3gguumw3aoue7atphe'))
    seleniumcommon.handle_window(driver, parent_handle)

def operation_completed():
    print("All operation completed => Enjoy")

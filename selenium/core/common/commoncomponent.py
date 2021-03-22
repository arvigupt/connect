from core.common.repository import data_platorm
from core.common.repository import login_path
from core.seleniumcore.pagefactory import seleniumcommon
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login_to_application(applicationname, username, password):
    data_platform_id = data_platorm.fetch_dataplatform_id(applicationname)
    sequences = login_path.fetch_login_path_sequence(data_platform_id)
    sequence_to_perform(sequences, username, password)


def sequence_to_perform(sequences, username, password):
    global url
    i = 1  # will remove this variable
    for operation in sequences:
        if (
                i != 9 and i != 10 and i != 11 and i != 12 and i != 13 and i != 14 and i != 15):  # will remove this if condition
            if operation['op_name'] == 'navigate-url':
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
                driver.get(url)
            if operation['op_name'] == 'verify':
                pagetovalidate = operation['element_identifier'].split('=', 1)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((pagetovalidate[0], pagetovalidate[1])))
            if operation['op_name'] == 'fill':
                type_and_value = operation['element_identifier'].split('=', 1)
                if (operation['element_key_value'] is None):
                    if (operation['element_key_name'] == 'username'):
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((type_and_value[0], type_and_value[1])))
                        seleniumcommon.type_into_element(driver, username,
                                                         type_and_value[0], type_and_value[1])
                    if (operation['element_key_name'] == 'password'):
                        WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((type_and_value[0], type_and_value[1])))
                        seleniumcommon.type_into_element(driver, password,
                                                         type_and_value[0], type_and_value[1])
                else:
                    seleniumcommon.type_into_element(driver, operation['element_key_value'],
                                                     type_and_value[0], type_and_value[1])
            if operation['op_name'] == 'click':
                type_and_value = operation['element_identifier'].split('=', 1)
                seleniumcommon.click(driver, type_and_value[0], type_and_value[1])
            if operation['op_name'] == 'check':
                type_and_value = operation['element_identifier'].split('=', 1)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((type_and_value[0], type_and_value[1])))
                if seleniumcommon.assert_radio_is_selected(driver, type_and_value[0], type_and_value[1]) == False:
                    seleniumcommon.click(driver, type_and_value[0], type_and_value[1])
            if operation['op_name'] == 'close-window':
                seleniumcommon.stopdriver(driver)
            if operation['op_name'] == 'save-mfa-session':
                url = driver.current_url
                print("Current to URL: {}".format(url))
                otpcookies = driver.get_cookies()
            if operation['op_name'] == 'save-login-session':
                url = driver.current_url
                print("Current to URL: {}".format(url))
                otpcookies = driver.get_cookies()
        i = i + 1  # will remove this variable condition


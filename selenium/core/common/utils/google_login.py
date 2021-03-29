from core.common.repository import dp_applicant_login_info
from core.seleniumcore.pagefactory import seleniumcommon
from core.common.models import login_credentails_dto
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from core.common import commoncomponent
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

username_element_key_name = "xpath=//input[@type='email']"
next_element_key_name = "xpath=//div[@class='VfPpkd-RLmnJb']"
password_element_key_name = "xpath=//input[@type='password']"
otp_element_key_name = "xpath=//input[@type='tel']"


def go_to(firsttimelogin):
    if (firsttimelogin == False):
        application_info = dp_applicant_login_info.fetch_dp_applicant_login_info(login_credentails_dto.data_platform_id)
        url = application_info['mfa_url']
        commoncomponent.add_drivers_to_path()
        login_credentails_dto.driver = webdriver.Chrome()
        login_credentails_dto.driver.implicitly_wait(5)
        print("Navigating to URL: {}".format(url))

        login_credentails_dto.driver.execute_cdp_cmd('Network.enable', {})
        for cookie in login_credentails_dto.temp_otpcookies:
            login_credentails_dto.driver.execute_cdp_cmd('Network.setCookie', cookie)
        login_credentails_dto.driver.execute_cdp_cmd('Network.disable', {})
        login_credentails_dto.driver.get(login_credentails_dto.temp_currenturl)
        windows_before = login_credentails_dto.driver.current_window_handle

        login_credentails_dto.driver.execute_cdp_cmd('Network.enable', {})
        for cookie in otpcookies:
            login_credentails_dto.driver.execute_cdp_cmd('Network.setCookie', cookie)
        login_credentails_dto.driver.execute_cdp_cmd('Network.disable', {})
        login_credentails_dto.driver.execute_script("window.open('{}')".format(url))
        windows_after = login_credentails_dto.driver.window_handles
        new_window = [x for x in windows_after if x != windows_before][0]
        login_credentails_dto.driver.switch_to_window(new_window)


def enter_credential(tenant_id, data_platform_id, applicant_id, username, password, otp):
    # verificationpin_locator = "id=idvPin"

    user_type_and_value = username_element_key_name.split('=', 1)
    if (seleniumcommon.is_element_visible(login_credentails_dto.driver, user_type_and_value[0], user_type_and_value[1])):
        next_type_and_value = next_element_key_name.split('=', 1)
        password_type_and_value = password_element_key_name.split('=', 1)
        seleniumcommon.type_into_element(login_credentails_dto.driver, username,
                                         user_type_and_value[0], user_type_and_value[1])
        seleniumcommon.click(login_credentails_dto.driver, next_type_and_value[0], next_type_and_value[1])
        WebDriverWait(login_credentails_dto.driver, 10).until(
            EC.element_to_be_clickable((password_type_and_value[0], password_type_and_value[1])))
        seleniumcommon.type_into_element(login_credentails_dto.driver, password,
                                         password_type_and_value[0], password_type_and_value[1])
        seleniumcommon.click(login_credentails_dto.driver, next_type_and_value[0], next_type_and_value[1])


        otp_type_and_value = otp_element_key_name.split('=', 1)
        if seleniumcommon.is_element_visible(login_credentails_dto.driver, otp_type_and_value[0], otp_type_and_value[1]):
            url = login_credentails_dto.driver.current_url
            cookies = login_credentails_dto.driver.get_cookies()
            dp_applicant_login_info.update_mfa_cookies(tenant_id, data_platform_id, applicant_id, url, cookies)
            dp_applicant_login_info.update_mfa_info(tenant_id, data_platform_id, applicant_id, True)
            applicant_login_info = dp_applicant_login_info.update_login_status(tenant_id, instruction[data_platform_id],
                                                                               applicant_id, 'google', 'in-progress')
            seleniumcommon.stopdriver(login_credentails_dto.driver)
            return True
        # pininput = verificationpin_locator.split('=', 1)
        # if seleniumcommon.is_element_visible(login_credentails_dto.driver, pininput[0], pininput[1]):
        #     currenturl = login_credentails_dto.driver.current_url
        #     print("Current to URL: {}".format(currenturl))
        #     otpcookies = login_credentails_dto.driver.get_cookies()
        #     dp_applicant_login_info.update_mfa_cookies(currenturl, login_credentails_dto.data_platform_id)
        #     seleniumcommon.stopdriver(login_credentails_dto.driver)
        #     return True
        else:
            i = 0
    return False


def enter_otp(otp):
    global otpcookies
    devicechecked_locator = "xpath=//div[contains(text(),'Don’t ask again on this device')]/parent::div/preceding-sibling::div"

    go_to(False)
    devicechecked_type_value = devicechecked_locator.split('=', 1)
    if seleniumcommon.assert_radio_is_selected(login_credentails_dto.driver, devicechecked_type_value[0], devicechecked_type_value[1]) == False:
        seleniumcommon.click(login_credentails_dto.driver, devicechecked_type_value[0], devicechecked_type_value[1])
    otpinput_type_value = otpinput_locator.split('=', 1)
    if seleniumcommon.is_element_visible(login_credentails_dto.driver, otpinput_type_value[0], otpinput_type_value[1]):
        next_element_key_name = next_locator.split('=', 1)
        seleniumcommon.type_into_element(login_credentails_dto.driver, input("Enter OTP received: "), otpinput_type_value[0], otpinput_type_value[1])
        seleniumcommon.click(login_credentails_dto.driver, next_element_key_name[0], next_element_key_name[1])
    # pininput = verificationpin_locator.split('=', 1)
    # if seleniumcommon.is_element_visible(login_credentails_dto.driver, pininput[0], pininput[1]):
    #     next_element_key_name = next_locator.split('=', 1)
    #     seleniumcommon.type_into_element(login_credentails_dto.driver, input("Enter OTP received on message: "), pininput[0], pininput[1])
    #     seleniumcommon.click(login_credentails_dto.driver, next[0], next[1])


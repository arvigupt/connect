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


# def go_to(driver, firsttimelogin):
#     if (firsttimelogin == False):
#         application_info = dp_applicant_login_info.fetch_dp_applicant_login_info(login_credentails_dto.data_platform_id)
#         url = application_info['mfa_url']
#         commoncomponent.add_drivers_to_path()
#         driver = webdriver.Chrome()
#         driver.implicitly_wait(5)
#         print("Navigating to URL: {}".format(url))
# 
#         driver.execute_cdp_cmd('Network.enable', {})
#         for cookie in login_credentails_dto.temp_otpcookies:
#             driver.execute_cdp_cmd('Network.setCookie', cookie)
#         driver.execute_cdp_cmd('Network.disable', {})
#         driver.get(login_credentails_dto.temp_currenturl)
#         windows_before = driver.current_window_handle
# 
#         driver.execute_cdp_cmd('Network.enable', {})
#         for cookie in otpcookies:
#             driver.execute_cdp_cmd('Network.setCookie', cookie)
#         driver.execute_cdp_cmd('Network.disable', {})
#         driver.execute_script("window.open('{}')".format(url))
#         windows_after = driver.window_handles
#         new_window = [x for x in windows_after if x != windows_before][0]
#         driver.switch_to_window(new_window)
# 

def enter_credential(driver, tenant_id, data_platform_id, applicant_id, username, password, otp):
    # verificationpin_locator = "id=idvPin"

    user_type_and_value = username_element_key_name.split('=', 1)
    if (seleniumcommon.is_element_visible(driver, user_type_and_value[0], user_type_and_value[1])):
        seleniumcommon.type_into_element(driver, username, user_type_and_value[0], user_type_and_value[1])
        next_type_and_value = next_element_key_name.split('=', 1)
        seleniumcommon.click(driver, next_type_and_value[0], next_type_and_value[1])
        password_type_and_value = password_element_key_name.split('=', 1)
        WebDriverWait(driver, 10).until( EC.element_to_be_clickable((password_type_and_value[0], password_type_and_value[1])))
        seleniumcommon.type_into_element(driver, password, password_type_and_value[0], password_type_and_value[1])
        seleniumcommon.click(driver, next_type_and_value[0], next_type_and_value[1])


        otp_type_and_value = otp_element_key_name.split('=', 1)
        if WebDriverWait(driver, 10).until(seleniumcommon.is_element_visible(driver, otp_type_and_value[0], otp_type_and_value[1])):
            url = driver.current_url
            cookies = driver.get_cookies()
            dp_applicant_login_info.update_mfa_cookies(tenant_id, data_platform_id, applicant_id, url, cookies, driver.session_id)
            dp_applicant_login_info.update_mfa_info(tenant_id, data_platform_id, applicant_id, True)
            applicant_login_info = dp_applicant_login_info.update_login_status(tenant_id, data_platform_id, applicant_id, 'google', 'in-progress')
        else:
            dp_applicant_login_info.update_login_cookies(tenant_id, data_platform_id, applicant_id, url, cookies)
            dp_applicant_login_info.update_login_status(tenant_id, data_platform_id, applicant_id, 'google', 'completed')
            dp_applicant_login_info.update_resume_from(tenant_id, data_platform_id, applicant_id, '')
    return True

# def enter_otp(driver, otp):
#     global otpcookies
#     devicechecked_locator = "xpath=//div[contains(text(),'Don’t ask again on this device')]/parent::div/preceding-sibling::div"
# 
#     go_to(False)
#     devicechecked_type_value = devicechecked_locator.split('=', 1)
#     if seleniumcommon.assert_radio_is_selected(driver, devicechecked_type_value[0], devicechecked_type_value[1]) == False:
#         seleniumcommon.click(driver, devicechecked_type_value[0], devicechecked_type_value[1])
#     otpinput_type_value = otpinput_locator.split('=', 1)
#     if seleniumcommon.is_element_visible(driver, otpinput_type_value[0], otpinput_type_value[1]):
#         next_element_key_name = next_locator.split('=', 1)
#         seleniumcommon.type_into_element(driver, input("Enter OTP received: "), otpinput_type_value[0], otpinput_type_value[1])
#         seleniumcommon.click(driver, next_element_key_name[0], next_element_key_name[1])
#     # pininput = verificationpin_locator.split('=', 1)
#     # if seleniumcommon.is_element_visible(driver, pininput[0], pininput[1]):
#     #     next_element_key_name = next_locator.split('=', 1)
#     #     seleniumcommon.type_into_element(driver, input("Enter OTP received on message: "), pininput[0], pininput[1])
#     #     seleniumcommon.click(driver, next[0], next[1])
# 

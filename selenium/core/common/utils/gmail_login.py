from core.common.repository import dp_applicant_login_info
from core.seleniumcore.pagefactory import seleniumcommon
from core.common.models import login_credentails_dto

global data_platform_id
global next_locator
global otpinput_locator

def go_to(data_platform_id, firsttimelogin):
    if (firsttimelogin == False):
        dp_applicant_login_info.fetch_dp_applicant_login_info(data_platform_id)
        url = dp_applicant_login_info['mfa_url']
        add_drivers_to_path()
        login_credentails_dto.driver = webdriver.Chrome()
        login_credentails_dto.driver.implicitly_wait(5)
        print("Navigating to URL: {}".format(url))

        login_credentails_dto.driver.execute_cdp_cmd('Network.enable', {})
        for cookie in otpcookies:
            login_credentails_dto.driver.execute_cdp_cmd('Network.setCookie', cookie)
        login_credentails_dto.driver.execute_cdp_cmd('Network.disable', {})
        login_credentails_dto.driver.get(url)


def enter_username_password(username, password):
    username_locator = "xpath=//input[@type='email']"
    next_locator = "xpath=//div[@class='VfPpkd-RLmnJb']"
    password_locator = "xpath=//input[@type='password']"
    otpinput_locator = "xpath=//input[@type='tel']"

    user_type_and_value = username_locator.split('=', 1)
    if (seleniumcommon.is_element_visible(login_credentails_dto.driver, user_type_and_value[0], user_type_and_value[1])):
        global otpcookies
        next_type_value = next_locator.split('=', 1)
        password_type_and_value = password_locator.split('=', 1)
        seleniumcommon.type_into_element(login_credentails_dto.driver, username,
                                         user_type_and_value[0], user_type_and_value[1])
        seleniumcommon.click(login_credentails_dto.driver, next_type_value[0], next_type_value[1])
        WebDriverWait(login_credentails_dto.driver, 10).until(
            EC.element_to_be_clickable((password_type_and_value[0], password_type_and_value[1])))
        seleniumcommon.type_into_element(login_credentails_dto.driver, password,
                                         password_type_and_value[0], password_type_and_value[1])
        seleniumcommon.click(login_credentails_dto.driver, next_type_value[0], next_type_value[1])
        otpinput = otpinput_locator.split('=', 1)
        if seleniumcommon.is_element_visible(login_credentails_dto.driver, otpinput[0], otpinput[1]):
            currenturl = login_credentails_dto.driver.current_url
            print("Current to URL: {}".format(currenturl))
            otpcookies = login_credentails_dto.driver.get_cookies()
            dp_applicant_login_info.update_mfa_cookies(currenturl,data_platform_id)
            seleniumcommon.stopdriver(login_credentails_dto.driver)
            return True
        pininput = databasedetails['verificationpin'].split('=', 1)
        if seleniumcommon.is_element_visible(login_credentails_dto.driver, pininput[0], pininput[1]):
            currenturl = login_credentails_dto.driver.current_url
            print("Current to URL: {}".format(currenturl))
            otpcookies = login_credentails_dto.driver.get_cookies()
            sql = "UPDATE quolum_db_schema.info SET otpurl = '{}' WHERE applicationname = '{}';".format(currenturl,
                                                                                                        applicationname)
            dbhelper.execute_update(sql)
            seleniumcommon.stopdriver(login_credentails_dto.driver)
            return True
    return False


def enter_otp(otp):
    global otpcookies
    devicechecked_locator = "//div[contains(text(),'Don’t ask again on this device')]/parent::div/preceding-sibling::div"
    go_to(data_platform_id, False)
    devicechecked_type_value = devicechecked_locator.split('=', 1)
    if seleniumcommon.assert_radio_is_selected(login_credentails_dto.driver, devicechecked_type_value, devicechecked_type_value) == False:
        seleniumcommon.click(login_credentails_dto.driver, devicechecked_type_value[0], devicechecked_type_value[1])
    otpinput_type_value = otpinput_locator.split('=', 1)
    if seleniumcommon.is_element_visible(login_credentails_dto.driver, otpinput_type_value[0], otpinput_type_value[1]):
        next_type_value = next_locator.split('=', 1)
        seleniumcommon.type_into_element(login_credentails_dto.driver, otp, otpinput_type_value[0], otpinput_type_value[1])
        seleniumcommon.click(login_credentails_dto.driver, next_type_value[0], next_type_value[1])
    pininput = databasedetails['verificationpin'].split('=', 1)
    if seleniumcommon.is_element_visible(login_credentails_dto.driver, pininput[0], pininput[1]):
        next = databasedetails['next'].split('=', 1)
        # seleniumcommon.type_into_element(login_credentails_dto.driver, userinput, pininput[0], pininput[1]) user input will take
        seleniumcommon.click(login_credentails_dto.driver, next[0], next[1])


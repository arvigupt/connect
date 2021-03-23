from core.common.repository import dp_applicant_login_info

global data_platform_id
global next_locator
global otpinput_locator

def go_to(driver ,data_platform_id, firsttimelogin):
    if (firsttimelogin == False):
        dp_applicant_login_info.fetch_dp_applicant_login_info(data_platform_id)
        url = dp_applicant_login_info['mfa_url']
        add_drivers_to_path()
        driver = webdriver.Chrome()
        driver.implicitly_wait(5)
        print("Navigating to URL: {}".format(url))

        driver.execute_cdp_cmd('Network.enable', {})
        for cookie in otpcookies:
            driver.execute_cdp_cmd('Network.setCookie', cookie)
        driver.execute_cdp_cmd('Network.disable', {})
    driver.get(url)


def enter_username_password(username, password):
    username_locator = "xpath=//input[@type='email']"
    next_locator = "//span[contains(text(),'Next')]/preceding-sibling::div"
    password_locator = "xpath=//input[@type='password']"
    otpinput_locator = "xpath=//input[@type='tel']"

    user_type_and_value = username_locator.split('=', 1)
    if (seleniumcommon.is_element_visible(driver, user_type_and_value[0], user_type_and_value[1])):
        global otpcookies

        next_type_value = next_locator.split('=', 1)
        password_type_and_value = password_locator.split('=', 1)
        seleniumcommon.type_into_element(driver, username,
                                         user_type_and_value[0], user_type_and_value[1])
        seleniumcommon.click(driver, next_type_value[0], next_type_value[1])
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((password_type_and_value[0], password_type_and_value[1])))
        seleniumcommon.type_into_element(driver, password,
                                         password_type_and_value[0], password_type_and_value[1])
        seleniumcommon.click(driver, next_type_value[0], next_type_value[1])
        otpinput = otpinput_locator.split('=', 1)
        if seleniumcommon.is_element_visible(driver, otpinput[0], otpinput[1]):
            currenturl = driver.current_url
            print("Current to URL: {}".format(currenturl))
            otpcookies = driver.get_cookies()
            dp_applicant_login_info.update_mfa_cookies(currenturl,data_platform_id)
            seleniumcommon.stopdriver(driver)
            return True
        pininput = databasedetails['verificationpin'].split('=', 1)
        if seleniumcommon.is_element_visible(driver, pininput[0], pininput[1]):
            currenturl = driver.current_url
            print("Current to URL: {}".format(currenturl))
            otpcookies = driver.get_cookies()
            sql = "UPDATE quolum_db_schema.info SET otpurl = '{}' WHERE applicationname = '{}';".format(currenturl,
                                                                                                        applicationname)
            dbhelper.execute_update(sql)
            seleniumcommon.stopdriver(driver)
            return True
    return False


def enter_otp(otp):
    global otpcookies
    devicechecked_locator = "//div[contains(text(),'Don’t ask again on this device')]/parent::div/preceding-sibling::div"
    go_to(driver, data_platform_id, False)
    devicechecked_type_value = devicechecked_locator.split('=', 1)
    if seleniumcommon.assert_radio_is_selected(driver, devicechecked_type_value, devicechecked_type_value) == False:
        seleniumcommon.click(driver, devicechecked_type_value[0], devicechecked_type_value[1])
    otpinput_type_value = otpinput_locator.split('=', 1)
    if seleniumcommon.is_element_visible(driver, otpinput_type_value[0], otpinput_type_value[1]):
        next_type_value = next_locator.split('=', 1)
        seleniumcommon.type_into_element(driver, otp, otpinput_type_value[0], otpinput_type_value[1])
        seleniumcommon.click(driver, next_type_value[0], next_type_value[1])
    pininput = databasedetails['verificationpin'].split('=', 1)
    if seleniumcommon.is_element_visible(driver, pininput[0], pininput[1]):
        next = databasedetails['next'].split('=', 1)
        # seleniumcommon.type_into_element(driver, userinput, pininput[0], pininput[1]) user input will take
        seleniumcommon.click(driver, next[0], next[1])


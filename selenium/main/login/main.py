from core.common import commoncomponent
from core.common.repository import data_platform
from core.common.repository import dp_applicant_login_info
from core.common.models.UserCredential import UserCredential
import uvicorn
import datetime
import json
import os
from typing import Optional
from fastapi import FastAPI, Header

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options as FirefoxOptions


login_status = 'login_status'
# async_mode = None
app = FastAPI()
# thread = None
# thread_lock = Lock()
# session_id = None


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def convert_response_into_json(result):
    return json.dumps(result, indent = 2, default = default)

def check_authorization_value(authorization):
    if authorization != "success":
        raise "invalid authorization"


@app.get("/platforms")
def get_platforms(authorization: Optional[str] = Header(None)):
    check_authorization_value(authorization)
    result = data_platform.fetch_data_platforms()
    return convert_response_into_json(result)

@app.get("/platforms/{platform_name}")
def get_platform_by_name(platform_name, authorization: Optional[str] = Header(None)):
    check_authorization_value(authorization)
    result = data_platform.fetch_data_platform_by_name(platform_name)
    return convert_response_into_json(result)


@app.post("/platforms")
def get_platforms(credential: UserCredential, authorization: Optional[str] = Header(None)):
    check_authorization_value(authorization)
    driver = get_grid_driver()
    result = start_login(driver, credential.tenant_id, credential.data_platform_id, credential.applicant_id, credential.username,
                         credential.password, credential.otp, credential.relogin)
    return convert_response_into_json(result)


def get_firefox_driver():
    options = FirefoxOptions()
    options.add_argument( "--window-size 1920,1080" )
    # options.add_argument( "--headless" )
    driver = Firefox( options=options )
    return driver


def get_remote_firefox(url):
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    options = FirefoxOptions()
    options.add_argument( "--window-size 1920,1080" )
    # options.add_argument( "--headless" )
    driver = webdriver.Remote( command_executor=url, desired_capabilities=firefox_capabilities )
    return driver


def get_remote_chrome(url):
    options = Options()
    options.add_argument( "no-sandbox" )
    options.add_argument( "--disable-dev-shm-usage" )
    options.add_argument( "--disable-infobars" )
    options.add_argument( '--disable-gpu' )  # Last I checked this was necessary.
    driver = webdriver.Remote( command_executor=url, desired_capabilities=options.to_capabilities() )
    return driver

def get_grid_driver():
    print("executing get_grid_driver")
    options = webdriver.ChromeOptions()
    options.add_argument( "no-sandbox" )
    options.add_argument( "--disable-gpu" )
    options.add_argument( "--incognito" )
    options.add_argument("--disable-infobars")
    options.add_argument( "--window-size=800,600" )
    options.add_argument( "--disable-dev-shm-usage" )
    driver = webdriver.Remote(
        command_executor="http://192.168.43.133:4444/wd/hub",
        desired_capabilities=DesiredCapabilities.CHROME, options=options )
    return driver



def start_login(driver, tenant_id, data_platform_id, applicant_id, username, password, otp, relogin):
    applicant_login_info = dp_applicant_login_info.fetch_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
    applicant_username = username
    applicant_pwd = password
    applicant_otp = otp

    if applicant_login_info == None:
        dp_applicant_login_info.insert_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
        dp_applicant_login_info.update_login_status(tenant_id, data_platform_id, applicant_id, '', "none")
        applicant_login_info = dp_applicant_login_info.fetch_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
    elif applicant_login_info[login_status] == "in-progress" :
        applicant_username = applicant_login_info['username']
        applicant_pwd = applicant_login_info['pwd']
    elif applicant_login_info[login_status] == "completed":
        if relogin == True:
            dp_applicant_login_info.delete_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
            dp_applicant_login_info.insert_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id)
            dp_applicant_login_info.update_login_status(tenant_id, data_platform_id, applicant_id, '', "none")
            applicant_login_info = dp_applicant_login_info.fetch_dp_applicant_login_info(tenant_id, data_platform_id,
                                                                                         applicant_id)
        else:
            print("Operation completed successfully.")
            exit(1)

    commoncomponent.login_to_application(driver, tenant_id, data_platform_id, applicant_id, applicant_username, applicant_pwd,
                                         applicant_otp, applicant_login_info)


# def reuse_browser(url, browser_id, p_otp):
#     driver = get_remote_chrome( url )
#     driver.close()
#     driver.quit()
#     driver.session_id = browser_id
#     auth_elem = driver.find_element_by_class_name( 'auth_code' )
#     sign_in_elem = driver.find_element_by_id( 'signin_btn' )
#     auth_elem.send_keys( p_otp )
#     sign_in_elem.click()
#     driver.implicitly_wait( 100 )
#     print( driver.current_url )
#     pickle.dump( driver.get_cookies(), open( "cookies.pkl", "wb" ) )
#     driver.quit()
#
#
# def reopen_session():
#     driver = get_grid_driver()
#     cookies = pickle.load( open( "cookies.pkl", "rb" ) )
#     driver.get( 'https://linkageapi.slack.com/' )
#     for cookie in cookies:
#         if 'expiry' in cookie:
#             cookie['expiry'] = int( cookie['expiry'] )
#         driver.add_cookie( cookie )
#     driver.refresh()
#     driver.get( 'https://linkageapi.slack.com/' )



if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
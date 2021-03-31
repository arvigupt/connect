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
app = FastAPI()
grid_url = "http://localhost:4444/wd/hub"

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
    driver = get_firefox_driver()
    result = start_login(driver, credential.tenant_id, credential.data_platform_id, credential.applicant_id, credential.username,
                         credential.password, credential.otp, credential.relogin)
    return convert_response_into_json(result)


def get_firefox_driver():
    print("executing get_firefox_driver")
    options = webdriver.FirefoxOptions()
    # options.add_argument( "no-sandbox" )
    # options.add_argument( "--disable-gpu" )
    options.add_argument( "-private" )
    # options.add_argument("--disable-infobars")
    # options.add_argument( "--disable-dev-shm-usage" )
    # options.add_argument("start-maximized");
    # options.add_argument("ignore-certificate-errors");
    # options.add_argument("disable-popup-blocking");
    # options.add_argument("disable-extensions");
    # options.add_argument("disable-notifications");
    driver = webdriver.Remote(command_executor=grid_url, desired_capabilities=DesiredCapabilities.FIREFOX, options=options )
    return driver


def get_chrome_driver():
    print("executing get_chrome_driver")
    options = webdriver.ChromeOptions()
    options.add_argument( "no-sandbox" )
    options.add_argument( "--disable-gpu" )
    options.add_argument( "--incognito" )
    options.add_argument("--disable-infobars")
    # options.add_argument( "--window-size=800,600" )
    options.add_argument( "--disable-dev-shm-usage" )
    options.add_argument("start-maximized");
    options.add_argument("ignore-certificate-errors");
    options.add_argument("disable-popup-blocking");
    options.add_argument("disable-extensions");
    options.add_argument("disable-notifications");
    # options.add_experimental_option("prefs", {"profile.allow_all_cookies": True});
    options.add_experimental_option("prefs", {"profile.enable-cookies": True});
    # options.add_argument("enable-cookies");
    # options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2});
    driver = webdriver.Remote(command_executor=grid_url, desired_capabilities=DesiredCapabilities.CHROME, options=options )
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


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
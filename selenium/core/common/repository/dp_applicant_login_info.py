from core.databaseconnect import dbhelper
import json


def insert_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id):
    sql = "INSERT INTO phyllo_schema.dp_applicant_login_info (tenant_id, data_platform_id, applicant_id) VALUES ('{}', '{}', '{}')".format(tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_insert(sql)

def delete_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id):
    sql = "DELETE FROM phyllo_schema.dp_applicant_login_info WHERE tenant_id = '{}' AND data_platform_id = '{}' " \
          "AND applicant_id = '{}'".format(tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_insert(sql)

def fetch_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id):
    sql = "SELECT * FROM phyllo_schema.dp_applicant_login_info WHERE tenant_id = '{}' AND data_platform_id = '{}' " \
          "AND applicant_id = '{}'".format(tenant_id, data_platform_id, applicant_id)
    result = dbhelper.execute_select(sql)
    if result != None and len(result) > 0:
        return result[0]
    return None

def update_mfa_cookies(tenant_id, data_platform_id, applicant_id, url, cookies):
    temp_cookies = str(cookies)
    temp_cookies = temp_cookies.replace("'", "''")
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET mfa_url = '{}', mfa_cookies = '{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        url, temp_cookies, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_login_cookies(tenant_id, data_platform_id, applicant_id, url, cookies):
    temp_cookies = str(cookies)
    temp_cookies = temp_cookies.replace("'", "''")
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET login_url = '{}', login_cookies = '{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        url, temp_cookies, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_username(tenant_id, data_platform_id, applicant_id, username):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET username = '{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        username, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_password(tenant_id, data_platform_id, applicant_id, password):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET pwd = '{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        password, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_login_status(tenant_id, data_platform_id, applicant_id, login_type, login_status):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET login_type = '{}', login_status = '{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        login_type, login_status, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_resume_from(tenant_id, data_platform_id, applicant_id, resume_from):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET resume_from = '{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        resume_from, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_mfa_info(tenant_id, data_platform_id, applicant_id, is_mfa_enabled):
    if is_mfa_enabled == True:
        sql = "UPDATE phyllo_schema.dp_applicant_login_info SET is_mfa_enabled = 't' WHERE tenant_id = '{}' AND " \
              "data_platform_id = '{}' AND applicant_id = '{}'".format(tenant_id, data_platform_id, applicant_id)
    else:
        sql = "UPDATE phyllo_schema.dp_applicant_login_info SET is_mfa_enabled = 'f' WHERE tenant_id = '{}' AND " \
              "data_platform_id = '{}' AND applicant_id = '{}'".format(tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

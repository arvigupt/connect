from core.databaseconnect import dbhelper


def insert_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id):
    sql = "INSERT INTO phyllo_schema.dp_applicant_login_info (tenant_id, data_platform_id, applicant_id) " \
          "VALUES ('{}', '{}', '{}')".format(tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_insert(sql)

def delete_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id):
    sql = "DELETE FROM phyllo_schema.dp_applicant_login_info WHERE tenant_id = '{}' AND data_platform_id = '{}' " \
          "AND applicant_id = '{}'".format(tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_insert(sql)

def fetch_dp_applicant_login_info(tenant_id, data_platform_id, applicant_id):
    sql = "SELECT * FROM phyllo_schema.dp_applicant_login_info WHERE tenant_id = '{}' AND data_platform_id = '{}' " \
          "AND applicant_id = '{}'".format(tenant_id, data_platform_id, applicant_id)
    return dbhelper.execute_select(sql)[0]

def update_mfa_cookies(tenant_id, data_platform_id, applicant_id, url, cookies):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET mfa_url = E'{}', mfa_cookies = E'{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        url, cookies, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_login_cookies(tenant_id, data_platform_id, applicant_id, url, cookies):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET login_url = E'{}', login_cookies = E'{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        url, cookies, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_username(tenant_id, data_platform_id, applicant_id, username):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET username = E'{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        username, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_password(tenant_id, data_platform_id, applicant_id, password):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET pwd = E'{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        password, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

def update_login_status(tenant_id, data_platform_id, applicant_id, login_status):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET login_status = E'{}' WHERE tenant_id = '{}' AND " \
          "data_platform_id = '{}' AND applicant_id = '{}'".format(
        login_status, tenant_id, data_platform_id, applicant_id)
    dbhelper.execute_update(sql)

from core.databaseconnect import dbhelper


def fetch_dp_applicant_login_info(data_platform_id):
    sql = "select * from phyllo_schema.dp_applicant_login_info where data_platform_id = '{}'".format(data_platform_id)
    return dbhelper.execute_select(sql)[0]

def update_mfa_cookies(currenturl, data_platform_id):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET mfa_url = '{}' WHERE data_platform_id = '{}';".format(
        currenturl, data_platform_id)
    dbhelper.execute_update(sql)

def update_login_cookies(currenturl, data_platform_id):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET login_url = '{}' WHERE data_platform_id = '{}';".format(
        currenturl, data_platform_id)
    dbhelper.execute_update(sql)

def update_username(username, data_platform_id):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET username = '{}' WHERE data_platform_id = '{}';".format(
        username, data_platform_id)
    dbhelper.execute_update(sql)

def update_password(password, data_platform_id):
    sql = "UPDATE phyllo_schema.dp_applicant_login_info SET pwd = '{}' WHERE data_platform_id = '{}';".format(
        password, data_platform_id)
    dbhelper.execute_update(sql)
from core.databaseconnect import dbhelper

def fetch_login_path_sequence(data_platform_id):
    sql = "select * from phyllo_schema.dp_login_path where data_platform_id = '{}' order by sequence_no".format(
        data_platform_id)
    return dbhelper.execute_select(sql)
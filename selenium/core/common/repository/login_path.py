from core.databaseconnect import dbhelper

def fetch_login_path_instructions(data_platform_id, level):
    if level is None:
        level = 1
    sql = "select * from phyllo_schema.dp_login_path where data_platform_id = '{}' and level = '{}' order by sequence_no".format(
        data_platform_id, level)
    return dbhelper.execute_select(sql)
from core.databaseconnect import dbhelper


def fetch_data_platform_id(data_platform_name):
    sql = "select id from phyllo_schema.data_platform where name = '{}'".format(data_platform_name)
    return dbhelper.execute_select(sql)[0]['id']


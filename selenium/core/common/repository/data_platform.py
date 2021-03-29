from core.databaseconnect import dbhelper


def fetch_data_platform_id(data_platform_name):
    sql = "select id from phyllo_schema.data_platform where name = '{}'".format(data_platform_name)
    return dbhelper.execute_select(sql)[0]['id']

def fetch_data_platforms():
    sql = "select * from phyllo_schema.data_platform"
    return dbhelper.execute_select(sql)


def fetch_data_platform_by_name(platform_name):
    sql = "select * from phyllo_schema.data_platform WHERE name = '{}'".format(platform_name)
    return dbhelper.execute_select(sql)

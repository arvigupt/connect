from core.databaseconnect import dbhelper


def fetch_dataplatform_id(applicationname):
    sql = "select id from phyllo_schema.data_platform where name = '{}'".format(applicationname)
    return dbhelper.execute_select(sql)[0]['id']


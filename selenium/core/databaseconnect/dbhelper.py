import psycopg2
import psycopg2.extras
from core.databaseconnect.config import config
import pdb


conn = None

def connect():
    try:
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return conn

# def execute_select(sql):
#     try:
#         temp_sql = "select row_to_json(row) from (" + sql + ") row"
#         with connect().cursor() as cur:
#             cur.execute(temp_sql)
#             rs_dict = cur.fetchall()
#     except Exception as e:
#         raise Exception("Failed running sql {}. Error: {}".format(sql, str(e)))
#
#     return rs_dict


def execute_select(sql, one=False):
    try:
        cur = connect().cursor()
        cur.execute(sql)
        r = [dict((cur.description[i][0], value) \
                   for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return (r[0] if r else None) if one else r
    except Exception as e:
        raise Exception("Failed running sql {}. Error: {}".format(sql, str(e)))


def execute_insert(sql):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        raise Exception("Failed running sql {}. Error: {}".format(sql, str(e)))


def execute_update(sql):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
    except Exception as e:
        raise Exception("Failed running sql {}. Error: {}".format(sql, str(e)))


if __name__ == '__main__':
    execute_select("select * from quolum_db_schema.info where applicationname = 'gmail'")


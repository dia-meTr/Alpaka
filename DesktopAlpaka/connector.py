import mysql.connector
from mysql.connector import FieldType
from constants import *

mydb = mysql.connector.connect(
    host=connection_params['host'],
    user=connection_params['user'],
    password=connection_params['password'],
    database=connection_params['database']
)
my_cursor = mydb.cursor()


def get_table_info(table):
    my_cursor.execute(f"SHOW columns FROM `{table}`")
    res = my_cursor.fetchall()

    my_cursor.execute(f"SELECT * FROM `{table}` LIMIT 1")
    my_cursor.fetchall()

    for i, desc in enumerate(my_cursor.description):
        res[i] = list(res[i])
        res[i][1] = FieldType.get_info(desc[1])
        res[i][2] = desc[6]
    print(res)

    return res


def get_relation(table, field_name):
    """
    function to get referenced columns
    """
    my_cursor.execute("SELECT `REFERENCED_TABLE_NAME`, `REFERENCED_COLUMN_NAME` "
                      "FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`"
                      f"WHERE `TABLE_NAME` = '{table}'  "
                      f"AND `COLUMN_NAME` = '{field_name}'")

    res = my_cursor.fetchall()[0]

    my_cursor.execute(f"SELECT `{res[1]}` FROM `{res[0]}`")

    return my_cursor.fetchall()

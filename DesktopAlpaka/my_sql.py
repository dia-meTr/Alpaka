"""frequently used functions that perform database queries"""

import mysql.connector
from mysql.connector import FieldType
from errors.error import MySQLError


def connect_to_bd(params):
    """This is function for connecting to BD"""
    mydb = mysql.connector.connect(
        host=params['host'],
        user=params['user'],
        password=params['password'],
        database=params['database']
    )
    my_cursor = mydb.cursor()

    return my_cursor, mydb


def get_privileges(user, cursor):
    """This is function for getting user's privileges"""
    try:
        cursor.execute(f"SELECT `Select_priv`, Insert_priv, Update_priv, Delete_priv "
                       f"FROM mysql.user WHERE `User`='{user}';")
        result = cursor.fetchall()
        print(result[0])
    except mysql.connector.errors.ProgrammingError:
        raise MySQLError("It seems like you don't have enough rights to use this app") \
            from mysql.connector.errors.ProgrammingError

    return result[0]


def get_table_info(table, cursor):
    """This is function for getting
    information about a table"""
    cursor.execute(f"SHOW columns FROM `{table}`")
    res = cursor.fetchall()

    cursor.execute(f"SELECT * FROM `{table}` LIMIT 1")
    cursor.fetchall()

    for i, desc in enumerate(cursor.description):
        res[i] = list(res[i])
        res[i][1] = FieldType.get_info(desc[1])
        res[i][2] = desc[6]
    print(res)

    return res


def get_relation(table, field_name, cursor):
    """This is function for getting referenced columns"""
    cursor.execute("SELECT `REFERENCED_TABLE_NAME`, `REFERENCED_COLUMN_NAME` "
                   "FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`"
                   f"WHERE `TABLE_NAME` = '{table}'  "
                   f"AND `COLUMN_NAME` = '{field_name}'")

    res = cursor.fetchall()[0]

    cursor.execute(f"SELECT `{res[1]}` FROM `{res[0]}`")

    return cursor.fetchall()


def get_tables(cursor):
    """This function gets all tables
    from BD and return a list of them"""
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    tables = [x[0] for x in result]
    return tables


def get_columns(table, cursor):
    """This function gets all columns
    from a table and return a list of them"""
    columns = []

    # If table variable is not empty:
    if table != '':
        # Executing SHOW columns... request
        cursor.execute(f"SHOW columns FROM `{table}`")
        res = cursor.fetchall()
        # print(res)

        # Creating list with columns
        columns = [x[0] for x in res]

    return columns

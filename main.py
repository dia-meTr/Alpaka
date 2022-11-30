import mysql.connector
from constants import *

mydb = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

mycursor = mydb.cursor()

mycursor.execute("Show tables;")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

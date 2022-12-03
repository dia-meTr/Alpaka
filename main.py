import mysql.connector
from constants import *
import tkinter as tk
from tkinter import ttk
from working_area import Main


mydb = mysql.connector.connect(
    host=connection_params['host'],
    user=connection_params['user'],
    password=connection_params['password'],
    database=connection_params['database']
)

print(mydb)

mycursor = mydb.cursor()

mycursor.execute("SELECT * from drink")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

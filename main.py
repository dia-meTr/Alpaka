import mysql.connector
from constants import *
import tkinter as tk
from working_area import Main

mydb = mysql.connector.connect(
    host=connection_params['host'],
    user=connection_params['user'],
    password=connection_params['password'],
    database=connection_params['database']
)
my_cursor = mydb.cursor()

if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("1100x600")
    m = Main(window, my_cursor)
    m.pack()

    window.mainloop()

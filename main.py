import mysql.connector
from constants import *
import tkinter as tk
from working_area import Main
from connector import my_cursor


if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("1100x600")
    m = Main(window, my_cursor)
    m.pack()

    window.mainloop()

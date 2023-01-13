"""
Welcome! It's an Alpaca designer of SQL queries
"""
import tkinter as tk
from tabs.working_area import WorkingArea
from tabs.connection_page import ConnectionPage
from my_sql import connect_to_bd


def connect(connection_params, privileges, page):
    """This is function for creating connection
    and displaying Working Area"""
    page.destroy()
    connection = connect_to_bd(connection_params)
    my_cursor = connection[0]
    mydb = connection[1]
    page = WorkingArea(app, my_cursor, mydb, privileges)
    page.pack()


if __name__ == '__main__':
    app = tk.Tk()
    app.geometry("1100x600")
    window = ConnectionPage(app, connect)
    window.pack(expand=True)

    app.mainloop()

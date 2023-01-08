import tkinter as tk
from working_area import WorkingArea
from DesktopAlpaka.connection_tab import ConnectionTab
from DesktopAlpaka.my_sql import connect_to_bd


def connect(connection_params, privileges):
    global window
    window.destroy()
    global mydb, my_cursor
    connection = connect_to_bd(connection_params)
    my_cursor = connection[0]
    mydb = connection[1]
    window = WorkingArea(app, my_cursor, mydb, privileges)
    window.pack()


if __name__ == '__main__':
    my_cursor = None
    mydb = None
    app = tk.Tk()
    app.geometry("1100x600")
    window = ConnectionTab(app, connect)
    window.pack(expand=True)

    app.mainloop()

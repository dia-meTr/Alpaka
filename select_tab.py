import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from table import Table
from sidebars import SidebarSelect


class SelectTab(Frame):
    def __init__(self, root, my_cursor):
        super().__init__(root)
        self.cursor = my_cursor
        self.table = tk.StringVar()
        self.table.trace('w', self.get_columns)
        columns = ('Drink_Name', 'Price', 'Size', 'Type')

        self.columnconfigure(0, weight=3, uniform='column')
        self.rowconfigure(0, weight=1, uniform='row')
        self.columnconfigure(1, weight=8, uniform='column')
        self.rowconfigure(1, weight=1, uniform='row')

        self.sb = SidebarSelect(self, relief=tk.RIDGE, borderwidth=5)
        self.m_space = tk.Frame(self, relief=tk.RIDGE, borderwidth=5)
        self.tb = Table(self, relief=tk.RIDGE, borderwidth=5)
        self.sb.grid(row=0, column=0, sticky="nsew")
        self.m_space.grid(row=0, column=1, sticky="nsew")
        self.tb.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # self.select(columns)
        self.sb.init_ui(columns)
        self.init_ui()

    def init_ui(self):
        self.cursor.execute("SHOW TABLES")
        result = self.cursor.fetchall()
        tables = [x[0] for x in result]
        print(tables)

        combox = ttk.Combobox(self.m_space, values=tables, textvariable=self.table)
        combox.grid()

        b = tk.Button(self.m_space, text='Select', command=self.select)
        b.grid()

    def select(self):
        print(self.table.get())
        c = self.sb.get_fields()
        print(c)
        self.cursor.execute(f"SELECT {', '.join(self.sb.get_fields())} from `{self.table.get()}`")
        result = self.cursor.fetchall()

        self.tb.make_view(c, result)

    def get_columns(self, *args):
        if self.table.get() != '':
            print(f"SHOW columns FROM `{self.table.get()}`")
            self.cursor.execute(f"SHOW columns FROM `{self.table.get()}`")
            res = self.cursor.fetchall()
            columns = [x[0] for x in res]
            print(columns)
            self.sb.init_ui(columns)

import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from table import Table


class SelectTab(Frame):
    def __init__(self, root, mycursor):
        super().__init__()
        self.cursor = mycursor
        self.table = tk.StringVar()
        self.table.trace('w', self.get_columns)
        columns = ('Drink_Name', 'Price', 'Size', 'Type')

        self.columnconfigure(0, weight=3, uniform='column')
        self.rowconfigure(0, weight=1, uniform='row')
        self.columnconfigure(1, weight=8, uniform='column')
        self.rowconfigure(1, weight=1, uniform='row')

        self.fr1 = SidebarSelect(self, relief=tk.RIDGE, borderwidth=5)
        self.fr2 = tk.Frame(self, relief=tk.RIDGE, borderwidth=5)
        self.fr3 = Table(self, relief=tk.RIDGE, borderwidth=5)
        self.fr1.grid(row=0, column=0, sticky="nsew")
        self.fr2.grid(row=0, column=1, sticky="nsew")
        self.fr3.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # self.select(columns)
        self.fr1.init_ui(columns)
        self.init_ui()

    def init_ui(self):
        self.cursor.execute("SHOW TABLES")
        result = self.cursor.fetchall()
        tables = [x[0] for x in result]
        print(tables)

        combox = ttk.Combobox(self.fr2, values=tables, textvariable=self.table)
        combox.grid()

        b = tk.Button(self.fr2, text='Select', command=self.select)
        b.grid()

    def select(self):
        print(self.table.get())
        c = self.fr1.get_fields()
        print(c)
        self.cursor.execute(f"SELECT {', '.join(self.fr1.get_fields())} from `{self.table.get()}`")
        result = self.cursor.fetchall()

        self.fr3.make_view(c, result)

    def get_columns(self, *args):
        if self.table.get() != '':
            print(f"SHOW columns FROM `{self.table.get()}`")
            self.cursor.execute(f"SHOW columns FROM `{self.table.get()}`")
            res = self.cursor.fetchall()
            columns = [x[0] for x in res]
            print(columns)
            self.fr1.init_ui(columns)


class SidebarSelect(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ch_all = None
        self.var_all = tk.BooleanVar()
        self.ch_buttons = {}

    def init_ui(self, columns):
        self.clear()
        self.ch_buttons = {}
        self.var_all.set(False)

        l = tk.Label(self, text='Select the fields to display')
        l.grid(row=0, column=0, columnspan=9, sticky='w')

        self.ch_all = tk.Checkbutton(self, text='All', variable=self.var_all, command=self.click_all)
        self.ch_all.grid(row=1, column=2, sticky='w')

        for i, column in enumerate(columns):
            var = tk.BooleanVar()
            ch = tk.Checkbutton(self, text=column, variable=var)
            ch.grid(row=i+2, column=1, columnspan=8, sticky='w')
            self.ch_buttons[column] = (ch, var)

    def click_all(self):
        if self.var_all.get():
            for ch in self.ch_buttons.values():
                ch[1].set(1)
        else:
            for ch in self.ch_buttons.values():
                ch[1].set(0)

    def get_fields(self):
        res = []
        for key, value in self.ch_buttons.items():
            if value[1].get():
                res.append(key)
        return res

    def clear(self):
        # destroy all widgets from frame
        for widget in self.winfo_children():
            widget.destroy()


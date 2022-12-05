import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from table import Table


class SelectTab(Frame):
    def __init__(self, root, mycursor):
        super().__init__()
        self.cursor = mycursor
        columns = ('Drink_Name', 'Price', 'Size', 'Type')

        self.columnconfigure(0, weight=2)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(1, weight=1)

        self.fr1 = SidebarSelect(self, width=300, height=300, relief=tk.RIDGE, borderwidth=5)
        self.fr2 = tk.Frame(self, width=800, height=300, relief=tk.RIDGE, borderwidth=5)
        self.fr3 = Table(self, width=1100, height=300, relief=tk.RIDGE, borderwidth=5)
        self.fr1.grid(row=0, column=0, sticky="nsew")
        self.fr2.grid(row=0, column=1, sticky="nsew")
        self.fr3.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # self.select(columns)
        self.fr1.init_ui(columns)
        self.init_ui()

    def init_ui(self):
        b = tk.Button(self.fr2, text='Select', command=self.select)
        b.grid()

    def select(self):
        c = self.fr1.get_fields()
        self.cursor.execute(f"SELECT {', '.join(c)} from drink")
        result = self.cursor.fetchall()

        self.fr3.make_view(c, result)


class SidebarSelect(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ch_all = None
        self.var_all = tk.BooleanVar()
        self.ch_buttons = {}

    def init_ui(self, columns):
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

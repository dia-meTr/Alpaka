import tkinter as tk
from tkinter import ttk
from table import Table


class SelectTab(ttk.Frame):
    def __init__(self, root, mycursor):
        super().__init__()
        self.cursor = mycursor
        columns = ('Drink_Name', 'Price', 'Size', 'Type')

        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)

        fr1 = tk.Frame(self, width=300, height=300, background='green')
        fr2 = tk.Frame(self, width=800, height=300, background='blue')
        self.fr3 = Table(self, width=1100, height=300, background='yellow')
        fr1.grid(row=1, column=1, sticky="nsew")
        fr2.grid(row=1, column=2, sticky="nsew")
        self.fr3.grid(row=2, column=1, columnspan=2, sticky="nsew")

        self.select(columns)

    def select(self, columns):
        self.cursor.execute(f"SELECT {', '.join(columns)} from drink")
        result = self.cursor.fetchall()

        self.fr3.make_view(columns, result)



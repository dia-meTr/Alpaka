import tkinter as tk
from tkinter import ttk


class InsertTab(ttk.Frame):
    def __init__(self, roo):
        super().__init__()

        fr1 = tk.Frame(self, width=300, height=300, background='green')
        fr2 = tk.Frame(self, width=800, height=300, background='pink')
        fr3 = tk.Frame(self, width=1100, height=300, background='yellow')
        fr1.grid(row=1, column=1)
        fr2.grid(row=1, column=2)
        fr3.grid(row=2, column=1, columnspan=2)

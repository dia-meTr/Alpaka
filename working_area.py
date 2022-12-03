import tkinter as tk
from tkinter import ttk
from insert_tab import InsertTab
from select_tab import SelectTab
from update_tab import UpdateTab
from delete_tab import DeleteTab


class Main(ttk.Frame):
    def __init__(self, root, mydb):
        super().__init__()
        tabControl = ttk.Notebook(root)

        self.tab_select = SelectTab(tabControl, mydb)
        self.tab_insert = InsertTab(tabControl)
        self.tab_update = UpdateTab(tabControl)
        self.tab_delete = DeleteTab(tabControl)

        tabControl.add(self.tab_select, text='SELECT')
        tabControl.add(self.tab_insert, text='INSERT')
        tabControl.add(self.tab_update, text='UPDATE')
        tabControl.add(self.tab_delete, text='DELETE')
        tabControl.pack(expand=1, fill="both")
        # self.build_tab()

    def build_tab(self):

        fr1 = tk.Frame(self.tab_insert, width=300, height=300, background='green')
        fr2 = tk.Frame(self.tab_insert, width=800, height=300, background='pink')
        fr3 = tk.Frame(self.tab_insert, width=1100, height=300, background='yellow')
        fr1.grid(row=1, column=1)
        fr2.grid(row=1, column=2)
        fr3.grid(row=2, column=1, columnspan=2)

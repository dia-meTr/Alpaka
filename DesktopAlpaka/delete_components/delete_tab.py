import tkinter as tk
from tkinter import ttk

from DesktopAlpaka.select_components.filter_data import Filter
from DesktopAlpaka.sidebar.sidebar import Sidebar
from DesktopAlpaka.base_classes.table import get_tables, Table, get_columns


class DeleteTab(tk.Frame):
    def __init__(self, root, my_cursor):
        super().__init__(root)
        self.chooser = None
        self.cursor = my_cursor
        self.tables = get_tables(self.cursor)

        self.table = tk.StringVar()
        self.table.trace('w', lambda *args: self.refresh_columns())

        self.columnconfigure(0, weight=3, uniform='column')
        self.rowconfigure(0, weight=1, uniform='row')
        self.columnconfigure(1, weight=8, uniform='column')
        self.rowconfigure(1, weight=1, uniform='row')

        self.side_bar = Sidebar(self, relief=tk.RIDGE, borderwidth=4)
        self.m_space = tk.Frame(self, relief=tk.RIDGE, borderwidth=4)
        self.table_view = Table(self, relief=tk.RIDGE, borderwidth=4)
        self.side_bar.grid(row=0, column=0, sticky="nsew")
        self.m_space.grid(row=0, column=1, sticky="nsew")
        self.table_view.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.side_bar.init_ui([])
        self.init_ui()

    def init_ui(self):
        table_chooser = ttk.Combobox(self.m_space, values=self.tables, textvariable=self.table)
        table_chooser.grid(row=0, column=0)

        delete_button = tk.Button(self.m_space, text='DELETE', command=self.get_query)
        delete_button.grid(row=0, column=1)

        self.chooser = Filter(self.m_space, get_columns(self.table.get(), self.cursor))
        self.chooser.init_ui()
        self.chooser.grid()

    def refresh_columns(self):
        columns = get_columns(self.table.get(), self.cursor)

        self.chooser.refresh(columns)

    def get_query(self):

        chooser = self.chooser.get_str()

        query = f"DELETE FROM `{self.table.get()}` " + chooser

        self.cursor.execute(query)

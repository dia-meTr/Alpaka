"""This module describes delete tab class"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from DesktopAlpaka.my_sql import get_tables, get_columns
from DesktopAlpaka.select_components.filter_data import Filter
from DesktopAlpaka.sidebar.sidebar import Sidebar
from DesktopAlpaka.base_classes.table import Table


class DeleteTab(tk.Frame):
    """
    This is class for delete tab
    """
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
        """
        This is methode for initialisation of UI
        """
        table_chooser = ttk.Combobox(self.m_space, values=self.tables, textvariable=self.table)
        table_chooser.grid(row=0, column=0)

        delete_button = tk.Button(self.m_space, text='DELETE', command=self.get_query)
        delete_button.grid(row=0, column=1)

        button_check = tk.Button(self.m_space, text='CHECK', command=self.check)
        button_check.grid(row=0, column=2)

        self.chooser = Filter(self.m_space, get_columns(self.table.get(), self.cursor))
        self.chooser.init_ui()
        self.chooser.grid()

    def get_table(self):
        """
        This is method for getting table and handling "No such table" error
        """
        if self.table.get() not in self.tables:
            raise Exception('There is no such table')
        else:
            return self.table.get()

    def check(self):
        """
        This methode execute Select query for chosen table
        """
        # Creating SQL request
        try:
            table = self.get_table()
            columns = self.side_bar.get_fields()
            sql_request = f"SELECT {', '.join(columns)} " \
                          f"from `{table}`;"
        except Exception as e:
            print(e.args)
            messagebox.showerror("Error", e.args[0])
            return

        # Execute SQL request
        print(sql_request)
        self.cursor.execute(sql_request)
        result = self.cursor.fetchall()

        # Build a table
        self.table_view.make_view(columns, result)

    def refresh_columns(self):
        """
        This is method for refreshing page after table was changed
        """
        columns = get_columns(self.table.get(), self.cursor)

        self.chooser.refresh(columns)
        self.side_bar.init_ui(columns)

    def get_query(self):
        """
        This is method for getting and executing DELETE query
        """

        chooser = self.chooser.get_str()

        query = f"DELETE FROM `{self.table.get()}` " + chooser

        self.cursor.execute(query)

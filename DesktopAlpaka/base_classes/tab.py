"""This module describes update tab class"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from DesktopAlpaka.sidebar.sidebar import Sidebar
from DesktopAlpaka.base_classes.table import Table
from DesktopAlpaka.my_sql import get_tables


class Tab(tk.Frame):
    """
    This is class for update tab
    """
    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    def __init__(self, root, my_cursor):
        super().__init__(root)
        self.head = None
        self.cursor = my_cursor
        self.tables = get_tables(self.cursor)
        self.table = tk.StringVar()
        self.table.trace('w', lambda *args: self.refresh_tab())

        # self.values_form = None
        # self.chooser = None

        # Rows&Columns configuration
        self.columnconfigure(0, weight=3, uniform='column')
        self.rowconfigure(0, weight=1, uniform='row')
        self.columnconfigure(1, weight=8, uniform='column')
        self.rowconfigure(1, weight=1, uniform='row')

        # Creating window parts
        self.side_bar = Sidebar(self, relief=tk.RIDGE, borderwidth=3)
        self.side_bar.grid(row=0, column=0, sticky="nsew")

        self.m_space = tk.Frame(self, relief=tk.RIDGE, borderwidth=3)
        self.m_space.grid(row=0, column=1, sticky="nsew")

        self.table_view = Table(self, relief=tk.RIDGE, borderwidth=3)
        self.table_view.grid(row=1, column=0, columnspan=2, sticky="nsew")

    def init_head(self):
        """
        This is methode for initialisation of UI
        """
        self.head = tk.Frame(self.m_space)
        self.head.grid(row=0, pady=5, padx=5)

        # Combobox for choosing table
        table_chooser = ttk.Combobox(self.head, values=self.tables, textvariable=self.table)
        table_chooser.grid(row=0, column=0, pady=5, padx=5)

        button_check = tk.Button(self.head, text='CHECK', command=self.check)
        button_check.grid(row=0, column=2, pady=5, padx=5)

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

    def refresh_tab(self):
        """
        refresh information in tab after changing table and will be
        overriden in all derived classes
        """
        pass

    def get_query(self):
        """
        This is methode for getting and executing query, and it will be
        overriden in all derived classes

        """
        pass

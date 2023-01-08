"""This module describes insert tab class"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from DesktopAlpaka.base_classes.table import Table
from DesktopAlpaka.sidebar.sidebar import Sidebar
from DesktopAlpaka.insert_components.insert_values_form import InsertValuesForm
from DesktopAlpaka.my_sql import get_columns, get_tables


class InsertTab(ttk.Frame):
    """
    This is class for Insert tab
    """
    def __init__(self, root, my_cursor):
        super().__init__(root)

        self.values_form = None
        self.table = tk.StringVar()
        self.table.trace('w', lambda *args: self.refresh_panel())
        self.cursor = my_cursor
        self.fields = []

        self.tables = get_tables(self.cursor)

        # Rows&Columns configuration
        self.columnconfigure(0, weight=3, uniform='column')
        self.rowconfigure(0, weight=1, uniform='row')
        self.columnconfigure(1, weight=8, uniform='column')
        self.rowconfigure(1, weight=1, uniform='row')

        self.side_bar = Sidebar(self, relief=tk.RIDGE, borderwidth=5)
        self.side_bar.grid(row=0, column=0, sticky="nsew")
        self.side_bar.init_ui(get_columns(self.table.get(), my_cursor))

        self.table_view = Table(self, relief=tk.RIDGE, borderwidth=5)
        self.table_view.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.m_space = tk.Frame(self, relief=tk.RIDGE, borderwidth=5)
        self.m_space.grid(row=0, column=1, sticky="nsew")
        self.init_ui()

    def init_ui(self):
        """
        This is methode for initialisation of UI
        """
        table_chooser = ttk.Combobox(self.m_space, values=self.tables, textvariable=self.table)
        table_chooser.grid(row=0, column=0)

        button_insert = tk.Button(self.m_space, text='INSERT', command=self.get_query)
        button_insert.grid(row=0, column=1)

        button_check = tk.Button(self.m_space, text='CHECK', command=self.check)
        button_check.grid(row=0, column=2)
        
        self.values_form = InsertValuesForm(self.m_space, self.cursor, self.table.get())
        self.values_form.grid(row=1)

    def refresh_panel(self):
        """
        refresh information panel after changing table
        """
        self.values_form.table = self.table.get()
        self.values_form.refresh_panel()

        self.side_bar.init_ui([el.field_name for el in self.values_form.fields])

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

    def get_query(self):
        """
        This is methode for getting and executing Insert query
        """
        form_data = self.values_form.get_values()

        columns = [row[0] for row in form_data]
        values = [row[1] for row in form_data]
        n_columns = len(columns)

        query = "INSERT INTO `" + self.table.get() + "` (`" + \
                '`, `'.join(columns) + "`) " \
                "VALUES (" + \
                ', '.join(["%s"] * n_columns) + ");"

        print(query, (columns, values))

        self.cursor.execute(query, (*values,))

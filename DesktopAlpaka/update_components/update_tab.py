"""This module describes update tab class"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from DesktopAlpaka.update_components.update_values_form import UpdateValuesForm
from DesktopAlpaka.select_components.filter_data import Filter
from DesktopAlpaka.sidebar.sidebar import Sidebar
from DesktopAlpaka.base_classes.table import Table
from DesktopAlpaka.my_sql import get_tables, get_columns


class UpdateTab(tk.Frame):
    """
    This is class for update tab
    """
    def __init__(self, root, my_cursor):
        super().__init__(root)
        self.new_values_form = None
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

        update_button = tk.Button(self.m_space, text='UPDATE', command=self.query_update)
        update_button.grid(row=0, column=1)

        button_check = tk.Button(self.m_space, text='CHECK', command=self.check)
        button_check.grid(row=0, column=2)

        insert_panel = tk.Frame(self.m_space, relief=tk.RIDGE, borderwidth=1)
        insert_panel.grid(column=0, row=1, sticky="nsew")

        where_panel = tk.Frame(self.m_space, relief=tk.RIDGE, borderwidth=1)
        where_panel.grid(column=1, row=1, sticky="nsew")

        self.m_space.columnconfigure(0, weight=1, uniform='column')
        self.m_space.rowconfigure(0, weight=1, uniform='row')
        self.m_space.columnconfigure(1, weight=1, uniform='column')
        self.m_space.rowconfigure(1, weight=5, uniform='row')

        self.chooser = Filter(where_panel, get_columns(self.table.get(), self.cursor))
        self.chooser.init_ui()
        self.chooser.grid()

        self.new_values_form = UpdateValuesForm(insert_panel, self.cursor, self.table.get())
        self.new_values_form.grid()

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
        refresh information panel after changing table
        """
        columns = get_columns(self.table.get(), self.cursor)
        self.new_values_form.table = self.table.get()
        self.new_values_form.refresh_panel()

        self.side_bar.init_ui(columns)

        self.chooser.refresh(columns)

    def query_update(self):
        """
        This is methode for getting and executing Update query
        """
        try:
            form_data = self.new_values_form.get_values()
            chooser = self.chooser.get_str()

            columns = [row[0] for row in form_data]
            values = [row[1] for row in form_data]

            query = "UPDATE `" + self.get_table() + "` SET `" + \
                    '` = %s '.join(columns) + "` = %s " + chooser

            self.cursor.execute(query, (*values,))

            messagebox.showinfo("Done", "Information updated")
        except Exception as e:
            print(e.args)
            messagebox.showerror("Error", e.args[0])
            return

"""This module describes update tab class"""

import tkinter as tk
from tkinter import messagebox
from update_components.update_values_form import UpdateValuesForm
from base_classes.filter.filter_data import Filter
from my_sql import get_columns
from base_classes.tab import Tab
from base_classes.Error import MySQLError


class UpdateTab(Tab):  # pylint: disable=too-many-ancestors
    """
    This is class for update tab
    """
    def __init__(self, root, my_cursor):
        super().__init__(root, my_cursor)
        self.new_values_form = None
        self.chooser = None

        self.side_bar.init_ui([])
        self.init_ui()

    def init_ui(self):
        """
        This is methode for initialisation of UI
        """
        self.init_head()

        update_button = tk.Button(self.head, text='UPDATE', command=self.get_query)
        update_button.grid(row=0, column=1, pady=5, padx=5)

        insert_panel = tk.Frame(self.m_space, relief=tk.RIDGE, borderwidth=1)
        insert_panel.grid(column=0, row=1, sticky="nsew")

        where_panel = tk.Frame(self.m_space, relief=tk.RIDGE, borderwidth=1)
        where_panel.grid(column=1, row=1, sticky="nsew")

        self.m_space.columnconfigure(0, weight=1, uniform='column')
        self.m_space.rowconfigure(0, weight=1, uniform='row')
        self.m_space.columnconfigure(1, weight=1, uniform='column')
        self.m_space.rowconfigure(1, weight=5, uniform='row')

        self.chooser = Filter(where_panel, get_columns(self.table.get(), self.cursor), self.update_scroll_region)
        self.chooser.init_ui()
        self.chooser.grid(pady=5, padx=5)

        self.new_values_form = UpdateValuesForm(insert_panel, self.cursor, self.table.get())
        self.new_values_form.grid(pady=5, padx=5, columnspan=50)

    def refresh_tab(self):
        """
        refresh information panel after changing table
        """
        columns = get_columns(self.table.get(), self.cursor)
        self.new_values_form.table = self.table.get()
        self.new_values_form.refresh_panel()

        self.side_bar.init_ui(columns)

        self.chooser.refresh(columns)
        
    def check(self):
        try:
            table = self.get_table()
            columns = self.side_bar.get_fields()
            sql_request = f"SELECT {', '.join(columns)} " \
                          f"from `{table}` " + self.chooser.get_str()
        except MySQLError as e:
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
        This is methode for getting and executing Update query
        """
        try:
            form_data = self.new_values_form.get_values()
            chooser = self.chooser.get_str()

            columns = [row[0] for row in form_data]
            values = [row[1] for row in form_data]

            query = "UPDATE `" + self.get_table() + "` SET `" + \
                    '` = %s, `'.join(columns) + "` = %s " + chooser
            print(query)

            self.cursor.execute(query, (*values,))

            messagebox.showinfo("Done", "Information updated")
        except MySQLError as ex:
            print(ex.args)
            messagebox.showerror("Error", ex.args[0])
            return

"""This module describes delete tab class"""

import tkinter as tk
from tkinter import messagebox
from my_sql import get_columns
from base_classes.filter.filter_data import Filter
from base_classes.tab import Tab
from base_classes.Error import MySQLError


class DeleteTab(Tab):  # pylint: disable=too-many-ancestors
    """
    This is class for delete tab
    """
    def __init__(self, root, my_cursor):
        super().__init__(root, my_cursor)
        self.chooser = None

        self.side_bar.init_ui([])
        self.init_ui()

    def init_ui(self):
        """
        This is methode for initialisation of UI
        """
        self.init_head()

        delete_button = tk.Button(self.head, text='DELETE', command=self.get_query)
        delete_button.grid(row=0, column=1)

        self.chooser = Filter(self.m_space, get_columns(self.table.get(), self.cursor), self.update_scroll_region)
        self.chooser.init_ui()
        self.chooser.grid(columnspan=50)

    def refresh_tab(self):
        """
        This is method for refreshing page after table was changed
        """
        if self.table.get() not in self.tables:
            return
        columns = get_columns(self.table.get(), self.cursor)

        self.chooser.refresh(columns)
        self.side_bar.init_ui(columns)

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
        This is method for getting and executing DELETE query
        """
        try:
            chooser = self.chooser.get_str()

            query = f"DELETE FROM `{self.get_table()}` " + chooser

            self.cursor.execute(query)

            messagebox.showinfo("Done", "Information deleted")

        except Exception as e:
            print(e.args)
            messagebox.showerror("Error", e.args[0])
            return

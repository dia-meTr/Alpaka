"""This is module for describing sort panel"""
import tkinter as tk
from tkinter import ttk
from my_sql import get_columns
from base_classes.error import MySQLError


class Sorter(tk.Frame):
    """This is class for sorting panel"""

    def __init__(self, root, my_cursor, table):
        super().__init__(root)

        self.columns = []
        self.column = tk.StringVar()
        self.reverse = tk.BooleanVar()
        self.cursor = my_cursor
        self.table = table
        self.cb_order_by = None

    def init_ui(self):
        """
        This is methode for initialising UI for sorting panel
        """
        lb_order_by = tk.Label(self, text='Order by:')
        lb_order_by.grid(row=1, column=0)
        self.columns = get_columns(self.table, self.cursor)

        self.cb_order_by = ttk.Combobox(self, values=self.columns,
                                        textvariable=self.column)
        self.cb_order_by.grid(row=1, column=1)

        ch_reverse = tk.Checkbutton(self, text="Reverse order", variable=self.reverse)
        ch_reverse.grid(row=1, column=2)

    def refresh(self, table, columns):
        """
        This method for refreshing form after table was changed
        """
        self.table = table
        self.columns = columns
        self.column.set('')
        self.cb_order_by['values'] = columns

    def get_query_piece(self):
        """
        This is method for getting piece of query responsible for sorting
        """
        result = ""
        column = self.column.get()

        if column != '' and column in self.columns:
            result += f" ORDER BY `{self.column.get()}`"

            if self.reverse.get():
                result += " DESC"
        elif column != '':
            raise MySQLError(f'There is no such column: {column}')

        return result

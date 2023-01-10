"""
This is module for building a filter
"""
import tkinter as tk
from tkinter import ttk
from base_classes.Error import MySQLError


class FilterBlock(tk.Frame):
    """
    This is class for a single block of Filters
    """
    def __init__(self, root, columns):
        super().__init__(root)
        self.columns = columns
        self.operators = {'Equal': '=',
                          'Not equal': '!=',
                          'Greater than': '>',
                          'Greater than or equal': '>=',
                          'Less than': '<',
                          'Less than or equal': '<='}

        self.column1 = tk.StringVar()
        self.operator_str = tk.StringVar()
        self.value = tk.StringVar()

        self.init_ui()

    def init_ui(self):
        """This is method that initialise UI of Filter Block"""
        filter_by = ttk.Combobox(self, values=self.columns, textvariable=self.column1)
        filter_by.grid(row=3, column=1, pady=5, padx=5)

        operator = ttk.Combobox(self, values=list(self.operators.keys()),
                                textvariable=self.operator_str)
        operator.grid(row=4, column=1, pady=5, padx=5)

        compare_with = ttk.Combobox(self, values=self.columns, textvariable=self.value)
        compare_with.grid(row=5, column=1, pady=5, padx=5)

    def is_full(self):
        """This is method that checks whether this block is full
        or some of its parts are missing"""
        return self.column1.get() != '' and self.operator_str.get() != '' and self.value.get() != ''

    def get_statement(self):
        """This method forms piece of sql request responsible
        for current filter"""
        statement = ""

        column = self.column1.get()
        operator = self.operator_str.get()
        value = self.value.get()

        if column in self.columns:
            statement += f"`{self.column1.get()}`"
        else:
            raise MySQLError(f"Unknown column {column}")
            return
        try:
            statement += f" {self.operators[operator]} "
        except KeyError:
            raise MySQLError(f"Unknown comparison string {operator}")
            return

        if value.lstrip("-").replace('.', '', 1).isnumeric():
            statement += value
        elif value in self.columns:
            statement += f"`{value}`"
        else:
            statement += f"'{value}'"

        return statement

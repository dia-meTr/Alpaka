import tkinter as tk
from tkinter import ttk


class FilterBlock(tk.Frame):
    """

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
        filter_by = ttk.Combobox(self, values=self.columns, textvariable=self.column1)
        filter_by.grid(row=3, column=1, pady=5, padx=5)

        operator = ttk.Combobox(self, values=list(self.operators.keys()), textvariable=self.operator_str)
        operator.grid(row=4, column=1, pady=5, padx=5)

        compare_with = ttk.Combobox(self, values=self.columns, textvariable=self.value)
        compare_with.grid(row=5, column=1, pady=5, padx=5)

    def is_full(self):
        return self.column1.get() != '' and self.operator_str.get() != '' and self.value.get() != ''

    def get_statement(self):
        statement = ""
        statement += f"`{self.column1.get()}`"
        statement += f" {self.operators[self.operator_str.get()]} "
        value = self.value.get()
        if value.lstrip("-").replace('.', '', 1).isnumeric():
            statement += value
        elif value in self.columns:
            statement += f"`{value}`"
        else:
            statement += f"'{value}'"

        return statement

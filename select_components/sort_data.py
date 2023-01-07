import tkinter as tk
from tkinter import ttk
from base_classes.table import get_columns


class Sorter(tk.Frame):
    def __init__(self, root, my_cursor, table):
        super().__init__(root)

        self.column = tk.StringVar()
        self.reverse = tk.BooleanVar()
        self.cursor = my_cursor
        self.table = table
        self.cb_order_by = None

    def init_ui(self):
        lb_order_by = tk.Label(self, text='Order by:')
        lb_order_by.grid(row=1, column=0)
        columns = get_columns(self.table, self.cursor)

        self.cb_order_by = ttk.Combobox(self, values=columns,
                                        textvariable=self.column)
        self.cb_order_by.grid(row=1, column=1)

        ch_reverse = tk.Checkbutton(self, text="Reverse order", variable=self.reverse)
        ch_reverse.grid(row=1, column=2)

    def refresh(self, table, columns):

        self.table = table
        self.cb_order_by['values'] = columns

    def get_query_piece(self):
        result = ""

        if self.column.get() != '':
            result += f" ORDER BY `{self.column.get()}`"

            if self.reverse.get():
                result += " DESC"

        return result






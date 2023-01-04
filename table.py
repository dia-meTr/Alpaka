import tkinter as tk
from tkinter import Frame
from tkinter import ttk


class Table(Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

    def make_view(self, columns, table):
        self.clear()

        tree = ttk.Treeview(self, column=columns, show='headings')
        tree.pack(expand=True, fill='both', side=tk.LEFT)

        for column in columns:
            tree.column(column, anchor=tk.CENTER)
            tree.heading(column, text=column)

        for row in table:
            tree.insert('', tk.END, values=row)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

    def clear(self):
        # destroy all widgets from frame
        for widget in self.winfo_children():
            widget.destroy()


def get_tables(cursor):
    cursor.execute("SHOW TABLES")
    result = cursor.fetchall()
    tables = [x[0] for x in result]
    return tables


def get_columns(table, cursor):
    columns = []

    # If table variable is not empty:
    if table.get() != '':
        # Executing SHOW columns... request
        cursor.execute(f"SHOW columns FROM `{table.get()}`")
        res = cursor.fetchall()
        # print(res)

        # Creating list with columns
        columns = [x[0] for x in res]

    return columns

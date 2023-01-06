import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from table import Table, get_columns, get_tables
from sidebars import SidebarSelect
from Insertion_panel import Field
from connector import get_table_info


class InsertTab(ttk.Frame):
    def __init__(self, root, my_cursor):
        super().__init__(root)

        self.table = tk.StringVar()
        self.table.trace('w', lambda *args: self.refresh_panel())
        self.cursor = my_cursor
        self.fields = []

        tables = get_tables(self.cursor)

        # Rows&Columns configuration
        self.columnconfigure(0, weight=3, uniform='column')
        self.rowconfigure(0, weight=1, uniform='row')
        self.columnconfigure(1, weight=8, uniform='column')
        self.rowconfigure(1, weight=1, uniform='row')

        self.side_bar = SidebarSelect(self, relief=tk.RIDGE, borderwidth=5)
        self.side_bar.grid(row=0, column=0, sticky="nsew")
        self.side_bar.init_ui(get_columns(self.table, my_cursor))

        self.table_view = Table(self, relief=tk.RIDGE, borderwidth=5)
        self.table_view.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.m_space = tk.Frame(self, my_cursor, relief=tk.RIDGE, borderwidth=5)
        self.m_space.grid(row=0, column=1, sticky="nsew")

        table_chooser = ttk.Combobox(self.m_space, values=tables, textvariable=self.table)
        table_chooser.grid(row=0, column=0)
        self.table.set(tables[0])

        button = tk.Button(self.m_space, text='INSERT', command=self.get_query)
        button.grid(row=0, column=1)

    def refresh_panel(self):
        """
        refresh information panel after changing table
        :return:
        """
        # If table variable is not empty:
        if self.table.get() != '':
            # Executing SHOW columns... request
            res = get_table_info(self.table.get())
            # print(res)

            for el in self.fields:
                el.grid_forget()

            self.fields = []

            for i, el in enumerate(res):
                self.fields.append(Field(self.m_space, self.cursor, self.table.get(), *el))
                self.fields[i].grid(row=i+1, column=0)

            self.side_bar.init_ui([el.field_name for el in self.fields])

    def get_query(self):
        args = []

        for el in self.fields:
            try:

                arg = el.get_value()
                if arg is not None:
                    args.append(arg)
            except Exception as e:
                print(e.args)
                messagebox.showerror("Error", e.args[0])
                return

        columns = [row[0] for row in args]
        values = [row[1] for row in args]
        n = len(columns)

        query = "INSERT INTO `" + self.table.get() + "` (`" + \
                '`, `'.join(columns) + "`) " \
                "VALUES (" + \
                ', '.join(["%s"] * n) + ");"

        print(query, (columns, values))

        self.cursor.execute(query, (*values,))



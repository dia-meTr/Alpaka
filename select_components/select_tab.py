import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Frame
from base_classes.table import Table, get_tables, get_columns
from sidebar.sidebar import Sidebar
from select_components.filter_data import Filter
from select_components.sort_data import Sorter


class SelectTab(Frame):
    """
    class for creating sql query
    """

    def __init__(self, root, my_cursor):
        super().__init__(root)
        self.cursor = my_cursor
        self.tables = get_tables(self.cursor)

        self.table = tk.StringVar()
        self.table.trace('w', lambda *args: self.refresh_columns())

        # Rows&Columns configuration
        self.columnconfigure(0, weight=3, uniform='column')
        self.rowconfigure(0, weight=1, uniform='row')
        self.columnconfigure(1, weight=8, uniform='column')
        self.rowconfigure(1, weight=1, uniform='row')

        # Creating window parts
        self.side_bar = Sidebar(self, relief=tk.RIDGE, borderwidth=5)
        self.m_space = tk.Frame(self, relief=tk.RIDGE, borderwidth=5)
        self.table_view = Table(self, relief=tk.RIDGE, borderwidth=5)
        self.side_bar.grid(row=0, column=0, sticky="nsew")
        self.m_space.grid(row=0, column=1, sticky="nsew")
        self.table_view.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Initialising UIs
        self.sort_block = Sorter(self.m_space, self.cursor, self.table.get())
        self.filter_chooser = None

        self.side_bar.init_ui([])
        self.init_ui()

    def init_ui(self):
        """
        Initialising UI for select tab
        :return:
        """

        # Combobox for choosing table
        cb_chose_table = ttk.Combobox(self.m_space, values=self.tables, textvariable=self.table)
        cb_chose_table.grid(row=0)

        # Order by
        self.sort_block = Sorter(self.m_space, self.cursor, self.table.get())
        self.sort_block.init_ui()
        self.sort_block.grid(row=1)

        # WHERE
        lb_where = tk.Label(self.m_space, text='Config filters')
        lb_where.grid(row=2, column=0)

        self.filter_chooser = Filter(self.m_space, [])
        self.filter_chooser.init_ui()
        self.filter_chooser.grid(row=3, column=0)

        # SELECT button
        select_button = tk.Button(self.m_space, text='Select', command=self.select)
        select_button.grid(row=0, column=50, sticky='es')

    def select(self):
        """
        Executing and formation of query
        """
        # Creating SQL request
        try:
            table = self.get_table()
            columns = self.side_bar.get_fields()
            sql_request = f"SELECT {', '.join(columns)} " \
                          f"from `{table}`"

            sql_request += self.filter_chooser.get_str()

            sql_request += self.sort_block.get_query_piece()
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

    def get_table(self):
        if self.table.get() not in self.tables:
            raise Exception('There is no such table')
        else:
            return self.table.get()

    def refresh_columns(self):
        """
        refreshing columns list for left sidebar and order_by checkbox
        """
        # Get columns in table
        columns = get_columns(self.table.get(), self.cursor)

        # Updating sidebar
        self.side_bar.init_ui(columns)

        self.sort_block.refresh(self.table.get(), columns)

        self.filter_chooser.refresh(columns)

import tkinter as tk
from tkinter import ttk
from tkinter import Frame
from table import Table, get_tables, get_columns
from sidebars import SidebarSelect
from filter_data import Filter


class SelectTab(Frame):
    """
    class for creating sql query
    """
    def __init__(self, root, my_cursor):
        super().__init__(root)
        self.filter_chooser = None
        self.bt_add_filter = None
        self.filters = []
        self.ch_reverse = None
        self.cb_order_by = None
        self.cursor = my_cursor
        self.table = tk.StringVar()
        self.order_by = tk.StringVar()
        self.reverse = tk.BooleanVar()
        self.table.trace('w', self.refresh_columns)
        columns = ('Drink_Name', 'Price', 'Size', 'Type')

        # Rows&Columns configuration
        self.columnconfigure(0, weight=3, uniform='column')
        self.rowconfigure(0, weight=1, uniform='row')
        self.columnconfigure(1, weight=8, uniform='column')
        self.rowconfigure(1, weight=1, uniform='row')

        # Creating window parts
        self.side_bar = SidebarSelect(self, relief=tk.RIDGE, borderwidth=5)
        self.m_space = tk.Frame(self, relief=tk.RIDGE, borderwidth=5)
        self.table_view = Table(self, relief=tk.RIDGE, borderwidth=5)
        self.side_bar.grid(row=0, column=0, sticky="nsew")
        self.m_space.grid(row=0, column=1, sticky="nsew")
        self.table_view.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Initialising UIs
        self.side_bar.init_ui(columns)
        self.init_ui()

    def init_ui(self):
        """
        Initialising UI for select tab
        :return:
        """
        # Get tables list
        tables = get_tables(self.cursor)

        # Combobox for choosing table
        cb_chose_table = ttk.Combobox(self.m_space, values=tables, textvariable=self.table)
        cb_chose_table.grid(row=0)

        # Order by
        lb_order_by = tk.Label(self.m_space, text='Order by:')
        lb_order_by.grid(row=1, column=0)

        self.cb_order_by = ttk.Combobox(self.m_space, values=get_columns(self.table, self.cursor),
                                        textvariable=self.order_by)
        self.cb_order_by.grid(row=1, column=1)

        self.ch_reverse = tk.Checkbutton(self.m_space, text="Reverse order", variable=self.reverse)
        self.ch_reverse.grid(row=1, column=2)

        # WHERE
        lb_where = tk.Label(self.m_space, text='Config filters')
        lb_where.grid(row=2, column=0)

        # self.bt_add_filter = tk.Button(self.m_space, text='+', command=self.add_filter)
        # self.bt_add_filter.grid(row=3, column=0)

        self.filter_chooser = Filter(self.m_space, self.cursor)
        self.filter_chooser.grid(row=3, column=0)

        # SELECT button
        select_button = tk.Button(self.m_space, text='Select', command=self.select)
        select_button.grid(row=0, column=50, sticky='es')

    def select(self):
        """
        Executing and formation of query
        """
        # Getting all posible columns
        columns = self.side_bar.get_fields()

        # Creating SQL request
        sql_request = ""
        if self.table.get() != '':
            sql_request += f"SELECT {', '.join(self.side_bar.get_fields())} from `{self.table.get()}`"
        else:
            return

        sql_request += self.filter_chooser.get_str()

        print(self.order_by.get())

        if self.order_by.get() != '':
            sql_request += f" ORDER BY `{self.order_by.get()}`"

        if self.reverse.get():
            sql_request += " DESC"

        # Execute SQL request
        print(sql_request)
        self.cursor.execute(sql_request)
        result = self.cursor.fetchall()

        # Build a table
        self.table_view.make_view(columns, result)

    def refresh_columns(self, *args):
        """
        refreshing columns list for left sidebar and order_by checkbox
        """
        # Get columns in table
        columns = get_columns(self.table, self.cursor)

        # Updating sidebar
        self.side_bar.init_ui(columns)

        self.cb_order_by['values'] = get_columns(self.table, self.cursor)

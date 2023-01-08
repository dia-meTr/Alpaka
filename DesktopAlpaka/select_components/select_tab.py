"""This module describes select tab class"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from DesktopAlpaka.my_sql import get_columns
from DesktopAlpaka.select_components.filter_data import Filter
from DesktopAlpaka.select_components.sort_data import Sorter
from DesktopAlpaka.base_classes.tab import Tab


class SelectTab(Tab):  # pylint: disable=too-many-ancestors
    """
    This is class for creating sql query
    """

    def __init__(self, root, my_cursor):
        super().__init__(root, my_cursor)

        # Initialising UIs
        self.sort_block = Sorter(self.m_space, self.cursor, self.table.get())
        self.filter_chooser = None

        self.side_bar.init_ui([])
        self.init_ui()

    def init_ui(self):
        """
        This is methode for initialising UI for select tab
        """

        # Combobox for choosing table
        chose_table = ttk.Combobox(self.m_space, values=self.tables, textvariable=self.table)
        chose_table.grid(row=0)

        # Order by
        self.sort_block = Sorter(self.m_space, self.cursor, self.table.get())
        self.sort_block.init_ui()
        self.sort_block.grid(row=1)

        # WHERE
        lb_where = tk.Label(self.m_space, text='Config filters')
        lb_where.grid(row=2, column=0)

        self.filter_chooser = Filter(self.m_space, [])
        self.filter_chooser.init_ui()
        self.filter_chooser.grid(row=3, column=0, columnspan=50)

        # SELECT button
        select_button = tk.Button(self.m_space, text='Select', command=self.get_query)
        select_button.grid(row=0, column=1, sticky='es')

    def get_query(self):
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

            self.cursor.execute(sql_request)
            result = self.cursor.fetchall()

        except Exception as ex:
            print(ex.args)
            messagebox.showerror("Error", ex.args[0])
            return

        # Execute SQL request
        print(sql_request)

        # Build a table
        self.table_view.make_view(columns, result)

    def refresh_tab(self):
        """
        This method is called when user change table name
        """
        # Get columns in table
        columns = get_columns(self.table.get(), self.cursor)

        # Updating sidebar
        self.side_bar.init_ui(columns)

        self.sort_block.refresh(self.table.get(), columns)

        self.filter_chooser.refresh(columns)

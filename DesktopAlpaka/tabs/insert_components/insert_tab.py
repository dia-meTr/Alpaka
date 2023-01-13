"""This module describes insert tab class"""

import tkinter as tk
from tkinter import messagebox
from tabs.insert_components.insert_values_form import InsertValuesForm
from tabs.tab import Tab
from base_classes.Error import MySQLError


class InsertTab(Tab):  # pylint: disable=too-many-ancestors
    """
    This is class for Insert tab
    """

    def __init__(self, root, my_cursor):
        super().__init__(root, my_cursor)

        self.values_form = None
        self.fields = []

        # Rows&Columns configuration
        self.init_ui()
        self.side_bar.init_ui([])

    def init_ui(self):
        """
        This is methode for initialisation of UI
        """
        self.init_head()

        button_insert = tk.Button(self.head, text='INSERT', command=self.get_query)
        button_insert.grid(row=0, column=1)

        self.values_form = InsertValuesForm(self.m_space, self.cursor, self.table.get())
        self.values_form.grid(row=1)

    def refresh_tab(self):
        """
        refresh information panel after changing table
        """
        if self.table.get() not in self.tables:
            return
        self.values_form.table = self.table.get()
        self.values_form.refresh_panel()

        self.side_bar.init_ui([el.field_name for el in self.values_form.fields])

        self.update_scroll_region()

    def get_query(self):
        """
        This is methode for getting and executing Insert query
        """
        try:
            table = self.get_table()
            form_data = self.values_form.get_values()

            columns = [row[0] for row in form_data]
            values = [row[1] for row in form_data]
            n_columns = len(columns)

            query = "INSERT INTO `" + table + "` (`" + \
                    '`, `'.join(columns) + "`) " \
                                           "VALUES (" + \
                    ', '.join(["%s"] * n_columns) + ");"

            self.cursor.execute(query, (*values,))

            messagebox.showinfo("Done", "Information added")

        except MySQLError as ex:
            print(ex.args)
            messagebox.showerror("Error", ex.args[0])
            return

        print(query, (columns, values))

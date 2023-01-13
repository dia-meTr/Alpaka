"""
This is module for value form class
It creates a form where user have to
enter new values for table
"""
import tkinter as tk
from values_form.field import Field
from my_sql import get_table_info


class ValuesForm(tk.Frame):
    """
    This is class for values form that is used in Insert and Update tabs
    """
    def __init__(self, root, my_cursor, table):
        super().__init__(root)

        self.table = table
        self.cursor = my_cursor
        self.fields = []

    def refresh_panel(self):
        """
        refresh information panel after changing table
        :return:
        """
        # If table variable is not empty:
        if self.table != '':
            # Executing SHOW columns... request
            res = get_table_info(self.table, self.cursor)
            # print(res)

            for field in self.fields:
                field.grid_forget()

            self.fields.clear()

            for i, field in enumerate(res):
                self.fields.append(self.new_field(field))
                self.fields[i].grid(row=i+1, column=0)

    def new_field(self, field_info):
        """
        This method creates new field for form
        """
        field = Field(self, self.cursor, self.table.get(), field_info)
        return field

    def get_values(self):
        """
        This method gets all values from the form
        """
        args = []

        for field in self.fields:

            arg = field.get_value()
            if arg is not None:
                args.append(arg)
        return args

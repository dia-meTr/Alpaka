import tkinter as tk
from tkinter import ttk
from constants import type_groups
from DesktopAlpaka.base_classes.DateTimePicker import DateTimePicker
from DesktopAlpaka.my_sql import get_relation


class Field(tk.Frame):
    """
    This is class for every field of table
    """
    def __init__(self, root, my_cursor, table, field_name, type_, null, key, default, extra):
        super().__init__(root)
        self.root = root
        self.cursor = my_cursor
        self.table = table

        self.field_name = field_name
        self.type = type_
        self.group_type = type_groups[type_]
        self.null = null
        self.key = key
        self.default = default
        self.extra = extra

        self.title = None
        self.block = None
        self.value = tk.StringVar()

        self.ui()

    def ui(self):
        """
        function that creates view of field depending on information about it
        """
        self.title = tk.Label(self, text=f'{self.field_name}\n({self.group_type}): ')

        if self.extra == 'auto_increment':
            self.block = tk.Label(self, text='Auto Increment')

        elif self.key == 'MUL':
            referenced_to = get_relation(self.table, self.field_name, self.cursor)
            self.block = ttk.Combobox(self, values=referenced_to, textvariable=self.value)

        elif self.group_type == 'datetime':
            self.block = tk.Label(self, text="")
            extra_block = tk.Button(self, text="SELECT DATE", command=self.ask_date)
            extra_block.grid(row=0, column=3)
        else:
            self.block = tk.Entry(self, textvariable=self.value)

        self.title.grid(row=0, column=0)
        self.block.grid(row=0, column=1)

    def get_value(self):
        """
        This is method for getting a pair of field name and its value
        """
        value = self.value.get()

        return self.field_name, value

    def check_type(self, value):
        """
        This is function for checkin whether value have right type
        """

        try:
            if self.group_type == 'number':
                value = int(value)
            elif self.group_type == 'float':
                value = float(value)
        except ValueError:
            raise Exception(f"Sorry, column '{self.field_name}' have to be {self.group_type}")

        return value

    def ask_date(self):
        """
        This function opens window for data picking
        """
        m = DateTimePicker(self.get_data, self.type)

    def get_data(self, date):
        """
        This function gets from DataTimePicker window
        """
        self.value.set(date)
        self.block['text'] = date

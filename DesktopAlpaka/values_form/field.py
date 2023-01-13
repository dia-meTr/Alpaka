"""This is module for fields class"""

import tkinter as tk
from tkinter import ttk
from constants import type_groups
from my_sql import get_relation
from values_form.DateTimePicker import DateTimePicker
from base_classes.Error import MySQLError


class Field(tk.Frame):
    """This is class for every field of table"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, root, my_cursor, table, field_description):
        super().__init__(root)
        self.referenced_to = None
        self.root = root
        self.cursor = my_cursor
        self.table = table

        self.field_name = field_description[0]
        self.type = field_description[1]
        self.group_type = type_groups[self.type]
        self.null = field_description[2]
        self.key = field_description[3]
        self.default = field_description[4]
        self.extra = field_description[5]

        self.title = None
        self.block = None
        self.value = tk.StringVar()

        self.init_ui()

    def init_ui(self):
        """Method that creates view of field depending on information about it"""
        self.title = tk.Label(self, text=f'{self.field_name}\n({self.group_type}): ')

        if self.extra == 'auto_increment':
            self.block = tk.Label(self, text='Auto Increment')

        elif self.key == 'MUL':
            referenced_to = get_relation(self.table, self.field_name, self.cursor)
            self.referenced_to = [_[0] for _ in referenced_to]
            self.block = ttk.Combobox(self, values=self.referenced_to, textvariable=self.value)

        elif self.group_type == 'datetime':
            self.block = tk.Label(self, text="")
            extra_block = tk.Button(self, text="SELECT DATE", command=self.ask_date)
            extra_block.grid(row=0, column=3)
        else:
            self.block = tk.Entry(self, textvariable=self.value)

        self.title.grid(row=0, column=0)
        self.block.grid(row=0, column=1)

    def get_value(self):
        """This is method for getting a pair of field name and its value"""
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
            raise MySQLError(f"Sorry, column '{self.field_name}' "
                             f"have to be {self.group_type}") from ValueError

        return value

    def ask_date(self):
        """
        This function opens window for data picking
        """
        _ = DateTimePicker(self.get_data, self.type)

    def get_data(self, date):
        """
        This function gets from DataTimePicker window
        """
        self.value.set(date)
        self.block['text'] = date

import tkinter as tk
from tkinter import ttk
from table import get_tables


class Field(tk.Frame):
    """
    class for every field of table
    """
    def __init__(self, root, my_cursor, table, field_name, type_, null, key, default, extra):
        super().__init__(root)
        self.root = root
        self.cursor = my_cursor
        self.table = table

        self.field_name = field_name
        self.type = type_
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
        self.title = tk.Label(self, text=f'{self.field_name}\n({self.type}): ')

        if self.extra == 'auto_increment':
            self.block = tk.Label(self, text='Auto Increment')

        elif self.key == 'MUL':
            # print(self.field_name)
            # print(self.table)
            referenced_to = self.get_relation()
            self.block = ttk.Combobox(self, values=referenced_to, textvariable=self.value)

        else:
            self.block = tk.Entry(self, textvariable=self.value)

        self.title.grid(row=0, column=0)
        self.block.grid(row=0, column=1)

    def get_relation(self):
        """
        function to get referenced columns
        """
        self.cursor.execute("SELECT `REFERENCED_TABLE_NAME`, `REFERENCED_COLUMN_NAME` "
                            "FROM `INFORMATION_SCHEMA`.`KEY_COLUMN_USAGE`"
                            f"WHERE `TABLE_NAME` = '{self.table}'  "
                            f"AND `COLUMN_NAME` = '{self.field_name}'")
        res = self.cursor.fetchall()[0]
        # print(res)

        self.cursor.execute(f"SELECT `{res[1]}` FROM `{res[0]}`")

        return self.cursor.fetchall()

    def get_value(self):
        value = self.value.get()
        if self.extra == 'auto_increment':
            return None
        elif value == '' and self.default is not None:
            value = self.default
        elif value == '' and self.null == 'NO':
            raise Exception(f"Sorry, column '{self.field_name}' can't be NULL")
        elif value == '' and self.null != 'NO':
            value = None

        if self.type == 'int':
            value = int(value)
        elif self.type == 'float':
            value = float(value)

        return self.field_name, value

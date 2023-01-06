import tkinter as tk
from tkinter import ttk
from table import get_columns


class FilterBlock(tk.Frame):
    """

    """
    def __init__(self, root, my_cursor):
        super().__init__(root)
        self.cursor = my_cursor
        self.table = tk.StringVar()
        self.table.set('drink')
        self.operators = {'Equal': '=',
                          'Not equal': '!=',
                          'Greater than': '>',
                          'Greater than or equal': '=>',
                          'Less than': '<',
                          'Less than or equal': '=<',
                          'Between a certain range': 'BETWEEN',
                          'Specify multiple possible values for a column': 'IN'}

        self.column1 = tk.StringVar()
        filter_by = ttk.Combobox(self, values=get_columns(self.table, self.cursor), textvariable=self.column1)
        filter_by.grid(row=3, column=1)

        self.operator_str = tk.StringVar()
        operator = ttk.Combobox(self, values=list(self.operators.keys()), textvariable=self.operator_str)
        operator.grid(row=4, column=1)

        self.value = tk.StringVar()
        compare_with = ttk.Combobox(self, values=get_columns(self.table, self.cursor), textvariable=self.value)
        compare_with.grid(row=5, column=1)

    def is_full(self):
        return self.column1.get() != '' and self.operator_str.get() != '' and self.value.get() != ''

    def get_statement(self):
        return f'{self.column1.get()} {self.operators[self.operator_str.get()]} {self.value.get()}'


class FiltersHolder(tk.Frame):
    def __init__(self, root, my_cursor):
        super().__init__(root, relief=tk.RAISED, borderwidth=5)
        self.cursor = my_cursor
        self.blocks = []
        self.count = 1

        block = FilterBlock(self, self.cursor)
        block.grid(row=0, column=self.count, rowspan=4)
        self.blocks.append(block)

        self.button = tk.Button(self, text='AND', command=self.click_and)
        self.button.grid(row=2, column=self.count + 1)

    def click_and(self):
        self.count += 1

        block = FilterBlock(self, self.cursor)
        block.grid(row=0, column=self.count, rowspan=4)
        self.blocks.append(block)

        self.button.grid(row=2, column=self.count + 1)

    def get_str(self):
        filters = []
        for i in range(self.count):
            if self.blocks[i].is_full():
                filters.append(self.blocks[i])

        if len(filters) == 0:
            return None

        filter_line = self.blocks[0].get_statement()

        if len(filters) > 1:
            for el in self.blocks[1:]:

                filter_line += ' AND '
                filter_line += el.get_statement()

        return '(' + filter_line + ')'


class Filter(tk.Frame):
    def __init__(self, root, cursor):
        super().__init__(root)
        self.count = 1
        self.block_holders = []
        self.cursor = cursor

        holder = FiltersHolder(self, self.cursor)
        holder.grid(row=self.count, column=0)
        self.block_holders.append(holder)

        self.button_or = tk.Button(self, text='OR', command=self.or_operator)
        self.button_or.grid(row=self.count + 1, column=0)

    def or_operator(self):
        self.count += 1

        holder = FiltersHolder(self, self.cursor)
        holder.grid(row=self.count, column=0)
        self.block_holders.append(holder)

        self.button_or.grid(row=self.count + 1, column=0)

    def get_str(self):
        filters = []
        for i in range(self.count):
            if self.block_holders[i].get_str() is not None:
                filters.append(self.block_holders[i])

        if len(filters) == 0:
            return ''

        filter_line = 'WHERE ' + self.block_holders[0].get_str()

        if len(filters) > 1:
            for el in self.block_holders[1:]:
                filter_line += ' OR '
                filter_line += el.get_str()

        return filter_line

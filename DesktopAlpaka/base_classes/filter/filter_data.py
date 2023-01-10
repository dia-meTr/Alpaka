"""
This is module for building a filter
"""
import tkinter as tk
from base_classes.filter.filter_block import FilterBlock


class FiltersHolder(tk.Frame):
    """
    This is class for a line of filters
    It build a line of filters connected with "and"
    and add new filter after pressing "AND" button
    """
    def __init__(self, root, columns, func):
        super().__init__(root, relief=tk.RAISED, borderwidth=3)
        self.columns = columns
        self.blocks = []
        self.count = 1
        self.button = None
        self.update_scroll_bar = func

        self.init_ui()

    def init_ui(self):
        """This is method that initialise UI of Filter Holder"""
        block = FilterBlock(self, self.columns)
        block.grid(row=0, column=self.count, rowspan=4)
        self.blocks.append(block)

        self.button = tk.Button(self, text='AND', command=self.click_and)
        self.button.grid(row=2, column=self.count + 1)

    def click_and(self):
        """This is method for adding new Filter Block to the line
        It's called when "AND" button is pressed"""

        self.count += 1

        block = FilterBlock(self, self.columns)
        block.grid(row=0, column=self.count, rowspan=4)
        self.blocks.append(block)

        self.button.grid(row=2, column=self.count + 1, pady=5, padx=5)
        self.update_scroll_bar()

    def get_str(self):
        """This method forms piece of sql request responsible
        for all filters inside of current holder"""
        filters = []
        for i in range(self.count):
            if self.blocks[i].is_full():
                filters.append(self.blocks[i])

        if len(filters) == 0:
            return None

        filter_line = self.blocks[0].get_statement()

        if len(filters) > 1:
            for block in self.blocks[1:]:

                filter_line += ' AND '
                filter_line += block.get_statement()

        return '(' + filter_line + ')'


class Filter(tk.Frame):
    """"""
    def __init__(self, root, columns, func):
        super().__init__(root)
        self.columns = columns
        self.count = 1
        self.block_holders = []
        self.button_or = None
        self.update_scroll_bar = func

    def init_ui(self):
        """This is method that initialise UI of Filter Block"""
        holder = FiltersHolder(self, self.columns, self.update_scroll_bar)
        holder.grid(row=self.count, column=0)
        self.block_holders.append(holder)

        self.button_or = tk.Button(self, text='OR', command=self.or_operator)
        self.button_or.grid(row=self.count + 1, column=0)

    def or_operator(self):
        """This is method for adding new Filter Holder to the Filter
        It's called when "OR" button is pressed"""
        self.count += 1

        holder = FiltersHolder(self, self.columns, self.update_scroll_bar)
        holder.grid(row=self.count, column=0)
        self.block_holders.append(holder)

        self.button_or.grid(row=self.count + 1, column=0, pady=5, padx=5)
        self.update_scroll_bar()

    def get_str(self):
        """This method forms piece of sql request responsible
        for filters"""
        filters = []
        for i in range(self.count):
            if self.block_holders[i].get_str() is not None:
                filters.append(self.block_holders[i])

        if len(filters) == 0:
            return ''

        filter_line = 'WHERE ' + self.block_holders[0].get_str()

        if len(filters) > 1:
            for holder in self.block_holders[1:]:
                filter_line += ' OR '
                filter_line += holder.get_str()

        return filter_line

    def refresh(self, columns):
        """This method cleans all filter holders and create one
        empty Filter Block as at the beginning"""
        self.columns = columns

        self.block_holders.clear()
        self.init_ui()

import tkinter as tk
from DesktopAlpaka.select_components.filter_block import FilterBlock


class FiltersHolder(tk.Frame):
    def __init__(self, root, columns):
        super().__init__(root, relief=tk.RAISED, borderwidth=5)
        self.columns = columns
        self.blocks = []
        self.count = 1
        self.button = None

        self.init_ui()

    def init_ui(self):
        block = FilterBlock(self, self.columns)
        block.grid(row=0, column=self.count, rowspan=4)
        self.blocks.append(block)

        self.button = tk.Button(self, text='AND', command=self.click_and)
        self.button.grid(row=2, column=self.count + 1)

    def click_and(self):
        self.count += 1

        block = FilterBlock(self, self.columns)
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
    def __init__(self, root, columns):
        super().__init__(root)
        self.columns = columns
        self.count = 1
        self.block_holders = []
        self.button_or = None

    def init_ui(self):
        holder = FiltersHolder(self, self.columns)
        holder.grid(row=self.count, column=0)
        self.block_holders.append(holder)

        self.button_or = tk.Button(self, text='OR', command=self.or_operator)
        self.button_or.grid(row=self.count + 1, column=0)

    def or_operator(self):
        self.count += 1

        holder = FiltersHolder(self, self.columns)
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

    def refresh(self, columns):
        self.columns = columns

        self.block_holders.clear()
        self.init_ui()
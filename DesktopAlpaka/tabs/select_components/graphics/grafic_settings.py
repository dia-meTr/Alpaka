"""This is module for settings of a graphic"""
import tkinter as tk
from tkinter import ttk, messagebox
from tabs.select_components.graphics.graphic import Graphic
from my_sql import get_table_info
from constants import type_groups


class GraphicSettings:
    """This is class for graphic settings"""
    def __init__(self, cursor):
        super().__init__()
        self.window = None
        self.cursor = cursor
        self.columns = []
        self.types = {}
        self.names_picker = None
        self.height_picker = None
        self.table = None

    def init_ui(self, filters, sorter):
        """This is methode for initialising"""
        self.window = tk.Toplevel()

        l_title = tk.Label(self.window, text="This is a chart customization tool")
        l_title.grid(row=0)

        l_columns = tk.Label(self.window, text="For columns")
        l_columns.grid(row=1, column=0)
        self.names_picker = ttk.Combobox(self.window, values=list(self.types.keys()))
        self.names_picker.grid(row=1, column=1)

        l_height = tk.Label(self.window, text="For their heights")
        l_height.grid(row=2, column=0)
        self.height_picker = ttk.Combobox(self.window, values=self.numbers_fields())
        self.height_picker.grid(row=2, column=1)

        draw_button = tk.Button(self.window, text="Draw",
                                command=lambda: self.draw(filters, sorter))
        draw_button.grid(row=3)

    def refresh(self, table, columns):
        """This is methode for refreshing settings"""
        self.table = table
        self.types.clear()
        self.columns = columns
        info = get_table_info(self.table, self.cursor)

        for item in info:
            self.types[item[0]] = item[1]

    def numbers_fields(self):
        """This is methode for getting a list of
        fields with number values"""
        numbers = []

        for key, value in self.types.items():
            if type_groups[value] in ['number', 'float', 'binary']:
                numbers.append(key)
        return numbers

    def draw(self, filters, sorter):
        """This is methode for creating a Graphic
        Called when "Draw" button is pressed"""
        names = self.names_picker.get()
        heights = self.height_picker.get()
        if names not in self.columns:
            messagebox.showerror("Error", f"No such column {names}")
            return
        if heights not in self.numbers_fields():
            messagebox.showerror("Error", f"No such number column {heights}")
            return

        graph = Graphic(self.cursor, self.table, names, heights)
        graph.draw(filters, sorter)

        self.window.destroy()

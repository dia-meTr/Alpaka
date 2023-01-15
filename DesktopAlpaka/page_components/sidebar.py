"""
This is module for left sidebar, where user
can select which fields to display in a table
"""
import tkinter as tk
from errors.error import MySQLError


class Sidebar(tk.Frame):
    """
    This is class for left sidebar
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ch_all = None
        self.var_all = tk.BooleanVar()
        self.ch_buttons = {}

    def init_ui(self, columns):
        """This is method for initialising UI of a sidebar"""
        # Clear old widgets
        self.clear()
        self.ch_buttons = {}
        self.var_all.set(False)

        # Label with instructions
        instruction_lb = tk.Label(self, text='Select the fields to display')
        instruction_lb.grid(row=0, column=0, columnspan=9, sticky='w')

        # "Select All" check button
        self.ch_all = tk.Checkbutton(self, text='All', variable=self.var_all,
                                     command=self.click_all)
        self.ch_all.grid(row=1, column=2, sticky='w')

        # Columns check buttons
        for i, column in enumerate(columns):
            var = tk.BooleanVar()
            ch_button = tk.Checkbutton(self, text=column, variable=var)
            ch_button.grid(row=i+2, column=1, columnspan=8, sticky='w')
            self.ch_buttons[column] = (ch_button, var)

    def click_all(self):
        """
        This is method for selecting all the check buttons
        Called when "All" checkbutton is clicked
        """
        if self.var_all.get():
            for ch_button in self.ch_buttons.values():
                # Make all check buttons selected
                ch_button[1].set(1)
        else:
            for ch_button in self.ch_buttons.values():
                # Make all check buttons UN-selected
                ch_button[1].set(0)

    def get_fields(self):
        """
        This is method for list with all
        selected fields
        """
        res = []
        for key, value in self.ch_buttons.items():
            if value[1].get():
                res.append(key)
        if not res:
            raise MySQLError("You have to choose at least one field")
        return res

    def clear(self):
        """
        This method clears delete all
        widgets in a sidebar
        """
        # destroy all widgets from frame
        for widget in self.winfo_children():
            widget.destroy()

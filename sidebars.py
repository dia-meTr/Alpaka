import tkinter as tk
from table import get_tables, get_columns


class SidebarSelect(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ch_all = None
        self.var_all = tk.BooleanVar()
        self.ch_buttons = {}

    def init_ui(self, columns):
        # Clear old widgets
        self.clear()
        self.ch_buttons = {}
        self.var_all.set(False)

        # Label with instructions
        lb = tk.Label(self, text='Select the fields to display')
        lb.grid(row=0, column=0, columnspan=9, sticky='w')

        # "Select All" check button
        self.ch_all = tk.Checkbutton(self, text='All', variable=self.var_all, command=self.click_all)
        self.ch_all.grid(row=1, column=2, sticky='w')

        # Columns check buttons
        for i, column in enumerate(columns):
            var = tk.BooleanVar()
            ch = tk.Checkbutton(self, text=column, variable=var)
            ch.grid(row=i+2, column=1, columnspan=8, sticky='w')
            self.ch_buttons[column] = (ch, var)

    def click_all(self):
        if self.var_all.get():
            for ch in self.ch_buttons.values():
                # Make all check buttons selected
                ch[1].set(1)
        else:
            for ch in self.ch_buttons.values():
                # Make all check buttons UN-selected
                ch[1].set(0)

    def get_fields(self):
        res = []
        for key, value in self.ch_buttons.items():
            if value[1].get():
                res.append(key)
        if not res:
            raise Exception(f"You have to choose at least one field")
        return res

    def clear(self):
        # destroy all widgets from frame
        for widget in self.winfo_children():
            widget.destroy()

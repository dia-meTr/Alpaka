import tkinter as tk
from tkinter import Frame


class SidebarSelect(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ch_all = None
        self.var_all = tk.BooleanVar()
        self.ch_buttons = {}

    def init_ui(self, columns):
        self.clear()
        self.ch_buttons = {}
        self.var_all.set(False)

        lb = tk.Label(self, text='Select the fields to display')
        lb.grid(row=0, column=0, columnspan=9, sticky='w')

        self.ch_all = tk.Checkbutton(self, text='All', variable=self.var_all, command=self.click_all)
        self.ch_all.grid(row=1, column=2, sticky='w')

        for i, column in enumerate(columns):
            var = tk.BooleanVar()
            ch = tk.Checkbutton(self, text=column, variable=var)
            ch.grid(row=i+2, column=1, columnspan=8, sticky='w')
            self.ch_buttons[column] = (ch, var)

    def click_all(self):
        if self.var_all.get():
            for ch in self.ch_buttons.values():
                ch[1].set(1)
        else:
            for ch in self.ch_buttons.values():
                ch[1].set(0)

    def get_fields(self):
        res = []
        for key, value in self.ch_buttons.items():
            if value[1].get():
                res.append(key)
        return res

    def clear(self):
        # destroy all widgets from frame
        for widget in self.winfo_children():
            widget.destroy()

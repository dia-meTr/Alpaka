"""This module describes how the Action tab is going to work"""
import json
import tkinter as tk
from tkinter import messagebox
import os


def clear_connect_info():
    params = {
        "host": "",
        "user": "",
        "password": "",
        "database": ""
    }
    json_params = json.dumps(params, indent=4)

    print(os.getcwd() + "/info.json")

    # Writing to sample.json
    with open("info.json", "w") as outfile:
        outfile.write(json_params)


def graph():
    """This is method for creating graph"""
    print("New Graphic")
    messagebox.showinfo("Done", "Graphic Created")


class ActionsTab(tk.Frame):
    """This is class for Action tab"""

    def __init__(self, root, cursor, conn):
        super().__init__(root)
        self.cursor = cursor
        self.conn = conn

        self.columnconfigure(0, weight=3, uniform='column')
        self.rowconfigure(0, weight=1, uniform='row')
        self.columnconfigure(1, weight=8, uniform='column')
        self.rowconfigure(1, weight=1, uniform='row')

        self.side_bar = tk.Frame(self, relief=tk.RIDGE, borderwidth=4)
        self.m_space = tk.Frame(self, relief=tk.RIDGE, borderwidth=4)
        self.table_view = tk.Frame(self, relief=tk.RIDGE, borderwidth=4)
        self.side_bar.grid(row=0, column=0, sticky="nsew")
        self.m_space.grid(row=0, column=1, sticky="nsew")
        self.table_view.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.init_ui()

    def init_ui(self):
        """This is method for initialising UI"""
        buttons = tk.Frame(self.m_space)
        buttons.pack(anchor=tk.CENTER)

        button_save = tk.Button(buttons, text="Save changes", command=self.save)
        button_save.grid(row=0, pady=5)

        button_revert = tk.Button(buttons, text="Revert changes", command=self.revert)
        button_revert.grid(row=1, pady=5)

        button_graph = tk.Button(buttons, text="Create graphic", command=graph)
        button_graph.grid(row=2, pady=5)

        button_clear_info = tk.Button(buttons, text="Clear connection info", command=clear_connect_info)
        button_clear_info.grid(row=3, pady=5)

    def save(self):
        """This is method for saving changes"""
        self.conn.commit()
        messagebox.showinfo("Done", "Changes Saved")

    def revert(self):
        """This is method for reverting changes"""
        self.conn.rollback()
        messagebox.showinfo("Done", "Changes Revert")

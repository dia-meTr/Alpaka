"""
This module describes working area of an app
Area, where five tabs are created and theirs classes are called
"""
from tkinter import ttk
import tkinter as tk
from tabs.insert_components.insert_tab import InsertTab
from tabs.select_components.select_tab import SelectTab
from tabs.update_components.update_tab import UpdateTab
from tabs.delete_components.delete_tab import DeleteTab
from tabs.actions_tab import ActionsTab


class WorkingArea(tk.Frame):
    """
    This class for working area
    """
    def __init__(self, root, my_cursor, conn, privileges):
        super().__init__()
        self.cursor = my_cursor
        self.conn = conn
        tab_control = ttk.Notebook(root)

        self.tab_select = SelectTab(tab_control, self.cursor)
        tab_control.add(self.tab_select, text='SELECT')

        if privileges[1] == 'Y':
            self.tab_insert = InsertTab(tab_control,  self.cursor)
            tab_control.add(self.tab_insert, text='INSERT')

        if privileges[2] == 'Y':
            self.tab_update = UpdateTab(tab_control,  self.cursor)
            tab_control.add(self.tab_update, text='UPDATE')

        if privileges[3] == 'Y':
            self.tab_delete = DeleteTab(tab_control,  self.cursor)
            tab_control.add(self.tab_delete, text='DELETE')

        self.tab_actions = ActionsTab(tab_control, self.cursor, self.conn)
        tab_control.add(self.tab_actions, text='ACTIONS')

        tab_control.pack(expand=1, fill="both")

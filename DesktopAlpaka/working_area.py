"""
This module describes working area of an app
Area, where five tabs are created and theirs classes are caled
"""
from tkinter import ttk
from DesktopAlpaka.insert_components.insert_tab import InsertTab
from DesktopAlpaka.select_components.select_tab import SelectTab
from DesktopAlpaka.update_components.update_tab import UpdateTab
from DesktopAlpaka.delete_components.delete_tab import DeleteTab
from DesktopAlpaka.actions_tab import ActionsTab


class WorkingArea(ttk.Frame):  # pylint: disable=too-many-ancestors
    """
    This class for working area
    """
    def __init__(self, root, my_cursor, conn):
        super().__init__()
        self.cursor = my_cursor
        tab_control = ttk.Notebook(root)

        self.tab_select = SelectTab(tab_control, self.cursor)
        self.tab_insert = InsertTab(tab_control,  self.cursor)
        self.tab_update = UpdateTab(tab_control,  self.cursor)
        self.tab_delete = DeleteTab(tab_control,  self.cursor)
        self.tab_actions = ActionsTab(tab_control, self.cursor, conn)

        tab_control.add(self.tab_select, text='SELECT')
        tab_control.add(self.tab_insert, text='INSERT')
        tab_control.add(self.tab_update, text='UPDATE')
        tab_control.add(self.tab_delete, text='DELETE')
        tab_control.add(self.tab_actions, text='ACTIONS')
        tab_control.pack(expand=1, fill="both")

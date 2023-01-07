from tkinter import ttk
from insert_components.insert_tab import InsertTab
from select_components.select_tab import SelectTab
from update_components.update_tab import UpdateTab
from delete_components.delete_tab import DeleteTab


class Main(ttk.Frame):
    def __init__(self, root, my_cursor):
        super().__init__()
        self.cursor = my_cursor
        tab_control = ttk.Notebook(root)

        self.tab_select = SelectTab(tab_control, self.cursor)
        self.tab_insert = InsertTab(tab_control,  self.cursor)
        self.tab_update = UpdateTab(tab_control,  self.cursor)
        self.tab_delete = DeleteTab(tab_control,  self.cursor)

        tab_control.add(self.tab_select, text='SELECT')
        tab_control.add(self.tab_insert, text='INSERT')
        tab_control.add(self.tab_update, text='UPDATE')
        tab_control.add(self.tab_delete, text='DELETE')
        tab_control.pack(expand=1, fill="both")

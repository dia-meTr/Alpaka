from tkinter import ttk
from tkinter import messagebox
from base_classes.field import Field
from connector import get_table_info


class ValuesForm(ttk.Frame):
    def __init__(self, root, my_cursor, table):
        super().__init__(root)

        self.table = table
        self.cursor = my_cursor
        self.fields = []

    def refresh_panel(self):
        """
        refresh information panel after changing table
        :return:
        """
        # If table variable is not empty:
        if self.table != '':
            # Executing SHOW columns... request
            res = get_table_info(self.table)
            # print(res)

            for el in self.fields:
                el.grid_forget()

            self.fields.clear()

            for i, el in enumerate(res):
                self.fields.append(self.new_field(el))
                self.fields[i].grid(row=i+1, column=0)

    def new_field(self, el):
        field = Field(self, self.cursor, self.table.get(), *el)
        return field

    def get_values(self):
        args = []

        for el in self.fields:
            try:
                arg = el.get_value()
                if arg is not None:
                    args.append(arg)
            except Exception as e:
                print(e.args)
                messagebox.showerror("Error", e.args[0])
                return

        return args

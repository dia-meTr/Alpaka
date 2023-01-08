import json
import tkinter as tk
from tkinter import messagebox
from DesktopAlpaka.my_sql import connect_to_bd, get_privileges
import mysql.connector


class ConnectionTab(tk.Frame):
    def __init__(self, root, func):
        super().__init__(root)
        self.params = None
        self.new_params = None
        self.func = func
        self.host = tk.StringVar()
        self.user = tk.StringVar()
        self.password = tk.StringVar()
        self.database = tk.StringVar()

        self.get_params()

        self.space = tk.Frame(self)
        self.space.pack(anchor=tk.CENTER)

        self.init_ui()

    def connect(self):
        self.new_params = {
            'host': self.host.get(),
            'user': self.user.get(),
            "password": self.password.get(),
            "database": self.database.get()
        }

        try:
            db = connect_to_bd(self.new_params)
            my_cursor = db[0]
            privileges = get_privileges(self.new_params['user'], my_cursor)
            my_cursor.close()
        except mysql.connector.errors.ProgrammingError as ex:
            print(ex.args)
            messagebox.showerror("Error", "Access denied")
            return
        except Exception as ex:
            print(ex)
            messagebox.showerror("Error", *ex.args)
            return

        if self.changes_applied():
            self.ask_to_save()

        self.func(self.new_params, privileges)

    def init_ui(self):
        tk.Label(self.space, text="Host", font=("Time", 18)).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.space, textvariable=self.host, font=("Time", 18)).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.space, text="User", font=("Time", 18)).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.space, textvariable=self.user, font=("Time", 18)).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.space, text="Password", font=("Time", 18)).grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.space, textvariable=self.password, font=("Time", 18), show="*").grid(row=2, column=1,
                                                                                           padx=5, pady=5)

        tk.Label(self.space, text="Database", font=("Time", 18)).grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(self.space, textvariable=self.database, font=("Time", 18)).grid(row=3, column=1, padx=5, pady=5)

        button = tk.Button(self.space, text="Confirm", command=self.connect, height=2)
        button.grid(row=5, column=1, columnspan=2, padx=20, pady=20)

    def get_params(self):
        with open("settings.json", 'r') as data:
            self.params = json.load(data)

        are_params_empty = self.params['user'] == ''

        if not are_params_empty:
            self.host.set(self.params['host'])
            self.user.set(self.params['user'])
            self.password.set(self.params['password'])
            self.database.set(self.params['database'])

    def set_params(self):
        json_params = json.dumps(self.new_params, indent=4)

        # Writing to sample.json
        with open("settings.json", "w") as outfile:
            outfile.write(json_params)

    def ask_to_save(self):
        res = messagebox.askquestion('Success', 'Do you wanna save data source parameters?')
        if res == 'yes':
            self.set_params()

    def changes_applied(self):
        if self.params['host'] != self.new_params['host']:
            return True

        if self.params['user'] != self.new_params['user']:
            return True

        if self.params['password'] != self.new_params['password']:
            return True

        if self.params['database'] != self.new_params['database']:
            return True

        return False

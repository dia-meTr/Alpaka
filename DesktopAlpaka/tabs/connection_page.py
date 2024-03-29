"""This is module for connection page"""
import json
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from my_sql import connect_to_bd, get_privileges
from errors.error import MySQLError


class ConnectionPage(tk.Frame):
    """This is class for connection page"""
    def __init__(self, root, func):
        super().__init__(root)
        self.params = None
        self.new_params = None
        self.func = func
        self.parameters = {'host': tk.StringVar(),
                           'user': tk.StringVar(),
                           'password': tk.StringVar(),
                           'database': tk.StringVar()}

        self.get_params()

        self.space = tk.Frame(self)
        self.space.pack(anchor=tk.CENTER)

        self.init_ui()

    def connect(self):
        """
        This is methode for connecting to BD and
        checking whether user have enough of rights
        """
        self.new_params = {
            'host': self.parameters['host'].get(),
            'user': self.parameters['user'].get(),
            "password": self.parameters['password'].get(),
            "database": self.parameters['database'].get()
        }

        try:
            database = connect_to_bd(self.new_params)
            my_cursor = database[0]
            privileges = get_privileges(self.new_params['user'], my_cursor)
            my_cursor.close()
        except mysql.connector.errors.ProgrammingError as ex:
            print(ex.args)
            messagebox.showerror("Error", "Access denied")
            return
        except MySQLError as ex:
            print(ex)
            messagebox.showerror("Error", *ex.args)
            return

        if self.changes_applied():
            self.ask_to_save()

        self.func(self.new_params, privileges, self)

    def init_ui(self):
        """
        This is methode for initialisation of UI
        """
        tk.Label(self.space, text="Host",
                 font=("Time", 18)).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.space, textvariable=self.parameters['host'],
                 font=("Time", 18)).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.space, text="User",
                 font=("Time", 18)).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.space, textvariable=self.parameters['user'],
                 font=("Time", 18)).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.space, text="Password",
                 font=("Time", 18)).grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.space, textvariable=self.parameters['password'],
                 font=("Time", 18), show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.space, text="Database",
                 font=("Time", 18)).grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(self.space, textvariable=self.parameters['database'],
                 font=("Time", 18)).grid(row=3, column=1, padx=5, pady=5)

        button = tk.Button(self.space, text="Confirm",
                           command=self.connect, height=2)
        button.grid(row=5, column=1, columnspan=2, padx=20, pady=20)

    def get_params(self):
        """
        This is methode for getting connection
        parameters from json file
        """
        filename = 'info.json'  # os.path.join(os.path.dirname(sys.executable), 'info.json')

        with open(filename, 'r', encoding="utf-8") as data:
            self.params = json.load(data)

        are_params_empty = self.params['user'] == ''

        if not are_params_empty:
            self.parameters['host'].set(self.params['host'])
            self.parameters['user'].set(self.params['user'])
            self.parameters['password'].set(self.params['password'])
            self.parameters['database'].set(self.params['database'])

    def set_params(self):
        """
        This is methode for saving connection
        parameters to json file
        """
        json_params = json.dumps(self.new_params, indent=4)
        filename = 'info.json'  # os.path.join(os.path.dirname(sys.executable), 'info.json')

        # Writing to sample.json
        with open(filename, "w", encoding="utf-8") as outfile:
            outfile.write(json_params)

    def ask_to_save(self):
        """
        This is methode for asking user do he/she
        wants to save connection parameters
        """
        res = messagebox.askquestion('Success', 'Do you wanna save data source parameters?')
        if res == 'yes':
            self.set_params()

    def changes_applied(self):
        """
        This is methode for checking whether user
        entered new connection parameters
        """
        if self.params['host'] != self.new_params['host']:
            return True

        if self.params['user'] != self.new_params['user']:
            return True

        if self.params['password'] != self.new_params['password']:
            return True

        if self.params['database'] != self.new_params['database']:
            return True

        return False

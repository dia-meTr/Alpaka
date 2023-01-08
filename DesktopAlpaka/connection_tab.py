import tkinter as tk
from tkinter import messagebox
import mysql.connector
from DesktopAlpaka.my_sql import connect_to_bd


class ConnectionTab(tk.Frame):
    def __init__(self, root, func):
        super().__init__(root)
        self.func = func
        self.host = tk.StringVar()
        self.user = tk.StringVar()
        self.password = tk.StringVar()
        self.database = tk.StringVar()

        self.space = tk.Frame(self)
        self.space.pack(anchor=tk.CENTER)

        entries = ['Host', 'User', 'Password', 'Database']
        variables = [self.host, self.user, self.password, self.database]

        for i, entry in enumerate(entries):
            label = tk.Label(self.space, text=entry, font=("Time", 18))
            label.grid(row=i, column=0, padx=5, pady=5)

            field = tk.Entry(self.space, textvariable=variables[i], font=("Time", 18))
            field.grid(row=i, column=1, padx=5, pady=5)

        button = tk.Button(self.space, text="Confirm", command=self.connect, height=2)
        button.grid(row=5, column=1, columnspan=2, padx=20, pady=20)

    def connect(self):
        params = {
            'host': self.host.get(),
            'user': self.user.get(),
            "password": self.password.get(),
            "database": self.database.get()
        }

        try:
            db = connect_to_bd(params)
            my_cursor = db[0]
        except Exception as e:
            messagebox.showerror("Error", "Error connecting")
            return

        my_cursor.close()
        self.func(params)

import tkinter as tk
from tkcalendar import *


class DateTimePicker(tk.Toplevel):
    def __init__(self, func, date, time, days):
        super().__init__()
        self.func = func
        self.date_needed = date
        self.time_needed = time
        self.days_needed = days

        self.cal = None

        self.time = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.days = [tk.StringVar(), tk.StringVar(), tk.StringVar()]

        if self.date_needed:
            self.data_chooser()

        if self.time_needed:
            self.time_chooser()

        if self.days_needed:
            self.days_chooser()

        submit_button = tk.Button(self, text="Submit", padx=10, pady=10,
                                  command=self.display_msg)
        submit_button.pack(pady=10)

    def data_chooser(self):
        frame_date = tk.Frame(self)
        frame_date.pack(pady=10)
        self.cal = Calendar(frame_date, selectmode="day", year=2023, month=1, day=11)
        self.cal.pack()

    def time_chooser(self):
        frame_time = tk.Frame(self)
        frame_time.pack(pady=10)
        f = ('Times', 20)

        minute = tk.Spinbox(frame_time, from_=0, to=23, wrap=True, textvariable=self.time[1],
                            width=2, state="readonly", font=f, justify=tk.CENTER)
        hours = tk.Spinbox(frame_time, from_=0, to=59, wrap=True, textvariable=self.time[0],
                           font=f, width=2, justify=tk.CENTER)

        seconds = tk.Spinbox(frame_time, from_=0, to=59, wrap=True, textvariable=self.time[2],
                             width=2, font=f, justify=tk.CENTER)

        minute.pack(side=tk.LEFT, fill=tk.X, expand=True)
        hours.pack(side=tk.LEFT, fill=tk.X, expand=True)
        seconds.pack(side=tk.LEFT, fill=tk.X, expand=True)

        msg = tk.Label(self, text="Hour  Minute  Seconds", font=("Times", 12))
        msg.pack(side=tk.TOP)

    def days_chooser(self):
        frame_days = tk.Frame(self)
        frame_days.pack(pady=10)
        f = ('Times', 20)

        months = tk.Spinbox(frame_days, from_=0, to=12, wrap=True, textvariable=self.days[1],
                            width=2, state="readonly", font=f, justify=tk.CENTER)
        years = tk.Spinbox(frame_days, from_=0, to=99, wrap=True, textvariable=self.days[0],
                           font=f, width=2, justify=tk.CENTER)

        days = tk.Spinbox(frame_days, from_=0, to=31, wrap=True, textvariable=self.days[2],
                          width=2, font=f, justify=tk.CENTER)

        years.pack(side=tk.LEFT, fill=tk.X, expand=True)
        months.pack(side=tk.LEFT, fill=tk.X, expand=True)
        days.pack(side=tk.LEFT, fill=tk.X, expand=True)
        msg = tk.Label(self, text="Years  Months  Days", font=("Times", 12))
        msg.pack(side=tk.TOP)

    def get_data(self):
        date = self.cal.selection_get()
        return date.strftime('%Y-%m-%d')

    def get_time(self):
        hours = self.time[0].get()
        minutes = self.time[1].get()
        seconds = self.time[2].get()
        return f"{minutes}:{hours}:{seconds}"

    def get_days(self):
        years = self.days[0].get()
        months = self.days[1].get()
        days = self.days[2].get()
        return f"{years}-{months}-{days}"

    def display_msg(self):
        res = ''
        if self.date_needed and self.time_needed:
            res = self.get_data() + ' ' + self.get_time()
        elif self.days_needed and self.time_needed:
            res = self.get_data() + ' ' + self.get_time()
        elif self.date_needed:
            res = self.get_data()
        elif self.days_needed:
            res = self.get_days()
        elif self.time_needed:
            res = self.get_time()

        print(res)
        self.func(res)
        self.destroy()



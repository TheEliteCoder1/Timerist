'''
The Resource package is a utility comprised of modules, classes, & functions                                                                                                 
that can help us easily break down implementations for GUI.

Module: time.py
Purpose: Access and Manage various units of time.
'''
from datetime import datetime, date, timedelta
import time

def days_in_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d %I:%M:%S %p")
    d2 = datetime.strptime(d2, "%Y-%m-%d %I:%M:%S %p")
    return abs((d2 - d1))

def get_date_range_list(start_date: date, end_date: date):
    dates = []
    delta = end_date - start_date  # returns timedelta
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        dates.append(day.strftime("%Y-%m-%d"))
    return dates

def get_current_time():
    fmt = datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
    fmtstr = f"{fmt}"
    return fmtstr

class StopWatch():
    def __init__(self):
        self.pause = 1

    def start_ticking_from_today(self, func):
        while True:
            current_date_and_time = datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
            func(current_date_and_time)
            time.sleep(self.pause)

class Date(date):
    pass
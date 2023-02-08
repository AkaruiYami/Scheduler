import math
import datetime
from types import new_class
import PySimpleGUI as sg

import timetable
import window as win
from models import model

TITLE = "Scheduler"


def init_empty_schedule():
    _headers = ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    schedule = model.Table(_headers)
    _date_today = datetime.date.today()
    start_time = datetime.datetime.combine(_date_today, datetime.time(hour=7, minute=0))
    end_time = datetime.datetime.combine(_date_today, datetime.time(hour=18, minute=0))
    interval = datetime.timedelta(hours=1)
    n_cell = math.ceil((end_time - start_time) / interval)

    time_str = lambda step: (start_time + interval * step).strftime("%I:%M%p")
    time_list = [time_str(i) for i in range(n_cell)]

    schedule.extend("Time", time_list)
    return schedule

    
table_window = timetable.TimetableWindow(TITLE, init_empty_schedule())
while True:
    event, values = table_window.read()

    if event == sg.WINDOW_CLOSED or event == "-CANCEL-":
        break

    if event == "-CONFIRM-":
        print(f"Title: {values['-TITLE-']}")
        print(f"Description: {values['-DESCRIPTION-']}")
    new_data = {}
    if event == "-ADD_BUTTON-":
        new_data = win.Window(TITLE).read(close=True)
    print(new_data)
table_window.close()

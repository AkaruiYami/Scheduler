import os
import sys
import pickle
import datetime
import PySimpleGUI as sg

import models
import ccolors
import layout as lyt

ROOT_DIR = os.path.dirname(sys.argv[0])
DATA_DIR = os.path.join(ROOT_DIR, "data")
timetable = models.Timetable("07:00AM", "06:00PM", 60)


def get_profile(idx=None, with_prefix=True, with_extension=True):
    saves = []
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for f in os.listdir(DATA_DIR):
        if f.endswith(".pkl") and "TABLE_" in f:
            if with_prefix == False:
                f = f.removeprefix("TABLE_")
            if with_extension == False:
                f = f.removesuffix(".pkl")
            saves.append(f)
    return saves[idx] if idx else saves


def remove_profile(name):
    name = filename_to_savename(name)
    target = os.path.join(DATA_DIR, name)
    if os.path.exists(target):
        os.remove(target)


def save_timetable(name):
    name = filename_to_savename(name)
    with open(os.path.join(DATA_DIR, name), "wb") as f:
        pickle.dump(timetable.get_raw_data(), f, protocol=pickle.HIGHEST_PROTOCOL)


def load_timetable(name):
    name = filename_to_savename(name)
    with open(os.path.join(DATA_DIR, name), "rb") as f:
        table = pickle.load(f)
        timetable.load(table)


def filename_to_savename(name):
    if not name.startswith("TABLE_"):
        name = "TABLE_" + name
    if not name.endswith(".pkl"):
        name = name + ".pkl"
    return name


def create_window(title, layout):
    window = sg.Window(title, layout=layout)
    return window


color = ccolors.get_color()
saves = get_profile(with_prefix=False, with_extension=False)
window = sg.Window(
    "Scheduler", layout=lyt.create_main_layout(saves, timetable), finalize=True
)
if saves:
    load_timetable(saves[0])

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "-ADD_BUTTON-":
        acw_event, acw_values = create_window(
            "Add New Schedule", lyt.create_input_laytout(timetable)
        ).read(close=True)
        if acw_event == "-CONFIRM-":
            day = acw_values["-DAY-"]
            time = acw_values["-TIME-"]
            # content = f'{acw_values["-TITLE-"]}\n{acw_values["-DESCRIPTION-"]}'
            content = models.Content(acw_values["-TITLE-"], acw_values["-DESCRIPTION-"])
            bg, fg = next(color)
            for i in range(acw_values["-DURATION-"]):
                _time = datetime.datetime.strptime(time, timetable.time_format)
                _dtime = datetime.timedelta(hours=i)
                actual_time = (_time + _dtime).strftime(timetable.time_format)
                timetable.update_content(day, actual_time, content, bg, fg)
    elif event == "-SAVE_BUTTON-":
        name = sg.popup_get_text("Name", "Save Timetable")
        if name:
            save_timetable(name)
            updated_files = get_profile(with_prefix=False, with_extension=False)
            window["-PROFILE-"].update(values=updated_files, value=name)
    elif event == "-DELETE_BUTTON-":
        result = sg.popup_ok_cancel("Are you sure you want to delete this timetable?")
        if result == "OK":
            files = get_profile(with_prefix=False, with_extension=False)
            current_profile = window["-PROFILE-"].get()
            files.remove(current_profile)
            window["-PROFILE-"].update(values=files)
            timetable.clear()
            remove_profile(current_profile)
    elif event == "-PROFILE-":
        filename = filename_to_savename(values["-PROFILE-"])
        load_timetable(filename)

    if str(event).endswith("+EDIT+"):
        event = event.rstrip("+EDIT+")
        day, time = event.split(",")
        cur_val = timetable[day][time]
        v = models.Content(*cur_val.get().split("\n"))
        edw_event, edw_values = create_window(
            "Add New Schedule",
            lyt.create_input_laytout(
                timetable,
                d_title=v.title,
                d_desc=v.description,
                d_day=day,
                d_time=time,
                edit=True,
            ),
        ).read(close=True)
        if edw_event == "-CONFIRM-":
            new_day = edw_values["-DAY-"]
            new_time = edw_values["-TIME-"]
            bg = cur_val.widget.cget("background")
            fg = cur_val.widget.cget("foreground")
            content = models.Content(edw_values["-TITLE-"], edw_values["-DESCRIPTION-"])
            timetable.delete_content(day, time)
            timetable.update_content(new_day, new_time, content, str(bg), str(fg))
        elif edw_event == "-DELETE-":
            timetable.delete_content(day, time)


window.close()

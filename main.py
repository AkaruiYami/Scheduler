import datetime
import PySimpleGUI as sg

import models
import ccolors

timetable = models.Timetable("07:00AM", "06:00PM", 60)


def header_cell(txt):
    t = sg.Text(
        "\n" + txt,
        relief=sg.RELIEF_RAISED,
        expand_x=True,
        size=(15, 3),
        justification="center",
    )
    return t


def content_cell(txt):
    t = sg.Text(txt, relief=sg.RELIEF_SUNKEN, expand_x=True, size=(15, 3))
    return t


def create_timetable_layout():
    layout = [[header_cell(txt) for txt in ["Time"] + timetable.days]]
    for time in timetable.time_frame:
        layout.append([header_cell(time)] + [ctx for ctx in timetable[time].values()])
    return layout


def create_main_layout():
    layout = [[sg.Push(), sg.Button("Add", key="-ADD_BUTTON-", size=10)]]
    timetable_layout = create_timetable_layout()
    layout.append(timetable_layout)
    return layout


window = sg.Window("Scheduler", layout=create_main_layout())


def create_window(
    title, d_title="", d_desc="", d_day=0, d_time=0, d_duration=0, edit=False
):
    label_size = (10, 1)
    layout = [
        _text_input("Title", size=label_size, default=d_title),
        _text_input("Description", size=label_size, default=d_desc),
        _element_selector("Day", timetable.days, size=label_size, default=d_day),
        _element_selector(
            "Time", timetable.time_frame, size=label_size, default=d_time
        ),
        _element_selector(
            "Duration",
            tuple(range(1, 10)),
            size=label_size,
            default=d_duration,
            visible=not edit,
        ),
        [
            sg.Push(),
            sg.Button("Cancel", key=lkey("Cancel")),
            sg.Button("Confirm", key="-CONFIRM-"),
            sg.Button("Delete", key="-DELETE-", visible=edit),
        ],
    ]
    window = sg.Window(title, layout=layout)
    return window


def _text_input(label, size=(None, None), key=None, default=""):
    if key is None:
        key = lkey(label)
    l = sg.Text(label, size=size)
    entry = sg.Input(key=key, default_text=default)
    return l, entry


def _element_selector(
    label, items, size=(None, None), key=None, default=0, visible=True
):
    if key is None:
        key = lkey(label)
    if isinstance(default, str):
        default = items.index(default)
    l = sg.Text(label, size=size, visible=visible)
    entry = sg.Combo(
        items,
        default_value=items[default],
        key=key,
        size=size[0] + 5,
        readonly=True,
        visible=visible,
    )
    return l, entry


def lkey(label):
    return f'-{label.upper().replace(" ", "_")}-'


color = ccolors.get_color()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "-ADD_BUTTON-":
        acw_event, acw_values = create_window("Add New Schedule").read(close=True)
        if acw_event == "-CONFIRM-":
            print(acw_values)
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
    if str(event).endswith("+EDIT+"):
        event = event.rstrip("+EDIT+")
        day, time = event.split(",")
        cur_val = timetable[day][time]
        v = models.Content(*cur_val.get().split("\n"))
        edw_event, edw_values = create_window(
            "Add New Schedule",
            d_title=v.title,
            d_desc=v.description,
            d_day=day,
            d_time=time,
            edit=True,
        ).read(close=True)
        print(edw_event, edw_values)
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

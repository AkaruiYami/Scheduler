import PySimpleGUI as sg

import models

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


def create_window(title):
    label_size = (10, 1)
    layout = [
        _text_input("Title", size=label_size),
        _text_input("Description", size=label_size),
        _element_selector("Day", timetable.days, size=label_size),
        _element_selector("Time", timetable.time_frame, size=label_size),
        [
            sg.Push(),
            sg.Button("Cancel", key=lkey("Cancel")),
            sg.Button("Confirm", key="-CONFIRM-"),
        ],
    ]
    window = sg.Window(title, layout=layout)
    return window


def _text_input(label, size=(None, None), key=None):
    if key is None:
        key = lkey(label)
    l = sg.Text(label, size=size)
    entry = sg.Input(key=key)
    return l, entry


def _element_selector(label, items, size=(None, None), key=None):
    if key is None:
        key = lkey(label)
    l = sg.Text(label, size=size)
    entry = sg.Combo(
        items,
        default_value=items[0],
        key=key,
        size=size[0] + 5,
        readonly=True,
    )
    return l, entry


def lkey(label):
    return f'-{label.upper().replace(" ", "_")}-'


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
            content = f'{acw_values["-TITLE-"]}\n{acw_values["-DESCRIPTION-"]}'
            timetable.update_content(day, time, content, "#0000a0")
window.close()

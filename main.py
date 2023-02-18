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
        layout.append(
            [header_cell(time)]
            + [content_cell(txt) for txt in timetable[time].values()]
        )
    return layout


layout = [[sg.Push(), sg.Button("Add", key="-ADD_BUTTON-", size=10)]]
timetable_layout = create_timetable_layout()
layout.append(timetable_layout)
window = sg.Window("Scheduler", layout=layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
window.close()

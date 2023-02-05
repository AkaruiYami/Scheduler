import PySimpleGUI as sg

import window as win


window = win.Window()
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == "-CANCEL-":
        break

    if event == "-CONFIRM-":
        print(f"Title: {values['-TITLE-']}")
        print(f"Description: {values['-DESC-']}")

window.close()

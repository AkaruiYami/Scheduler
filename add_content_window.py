import PySimpleGUI as sg


# TODO: Create a window to add new schedule
def create_window(title):
    layout = [_text_input("Title"), _text_input("Description")]
    window = sg.Window(title, layout=layout)
    return window


def _text_input(label, key=None):
    if key is None:
        key = f'-{label.upper().replace(" ", "_")}-'
    l = sg.Text(label)
    entry = sg.Input(key=key)
    return l, entry

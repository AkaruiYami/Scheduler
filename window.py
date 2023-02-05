import PySimpleGUI as sg

class Window(sg.Window):
    LABEL_SPACING = 30
    TEXT_SIZE = 50

    def __init__(self, title="Scheduler"):
        super().__init__(title)
        layout = [[Window.create_label_input("Title")],
                  [Window.create_label_input("Description", multiline=True)],
                  [Window.create_date_input("Date")],
                  [sg.Button("Confirm", key="-CONFIRM-"), sg.Button("Cancel", key="-CANCEL-")]]
        self.layout(layout)

    @staticmethod
    def create_label_input(text, placeholder=None, key=None, multiline=False):
        if placeholder is None:
            placeholder = ""
        if key is None:
            key = f"-{text.upper()}-"

        label = sg.Text(text, size=(Window.LABEL_SPACING, 1))
        if multiline:
            entry = sg.Multiline(placeholder, autoscroll=True, size=(Window.TEXT_SIZE, 3), key=key)
        else:
            entry = sg.Input(placeholder, size=(Window.TEXT_SIZE,1), key=key)

        return label, entry

    @staticmethod
    def create_date_input(text, placeholder=None, key=None):
        if placeholder is None:
            placeholder = ""
        if key is None:
            key = f"-{text.upper()}-"

        label = sg.Text(text, size=(Window.LABEL_SPACING, 1))
        entry = sg.Input(placeholder, key=key)
        cal_entry = sg.CalendarButton(text, close_when_date_chosen=True, target=key, location=(0, 0), no_titlebar=False)
        return label, entry, cal_entry
        

if __name__ == "__main__":
    window = Window("Scheduler")

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "-CANCEL-":
            break

        if event == "-CONFIRM-":
            print(values["-TITLE-"])
            print(values["-DESCRIPTION-"])

    window.close()

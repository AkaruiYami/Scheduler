import PySimpleGUI as sg


class Window(sg.Window):
    LABEL_SPACING = 10
    TEXT_SIZE = 50

    def __init__(self, title="Scheduler"):
        super().__init__(title)
        _days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
        ]
        layout = [
            [Window.create_label_input("Title")],
            [Window.create_label_input("Description", multiline=True)],
            [Window.create_combobox("Day", items=_days, default_item=_days[0])],
            [Window.create_time_selector("Start Time")],
            [
                Window.create_time_selector(
                    "Duration", active_selection=[True, True, False]
                )
            ],
            [
                sg.Stretch(),
                sg.Button("Confirm", key="-CONFIRM-"),
                sg.Button("Cancel", key="-CANCEL-"),
            ],
        ]
        self.layout(layout)

    @staticmethod
    def create_label_input(text, placeholder=None, key=None, multiline=False):
        if placeholder is None:
            placeholder = ""
        if key is None:
            key = f"-{text.strip().replace(' ', '_').upper()}-"

        label = sg.Text(text, size=(Window.LABEL_SPACING, 1))
        if multiline:
            entry = sg.Multiline(
                placeholder,
                autoscroll=True,
                size=(Window.TEXT_SIZE, 3),
                key=key,
            )
        else:
            entry = sg.Input(placeholder, size=(Window.TEXT_SIZE, 1), key=key)

        return label, entry

    @staticmethod
    def create_date_input(text, placeholder=None, key=None):
        if placeholder is None:
            placeholder = ""
        if key is None:
            key = f"-{text.strip().replace(' ', '_').upper()}-"

        label = sg.Text(text, size=(Window.LABEL_SPACING, 1))
        entry = sg.Input(placeholder, key=key)
        cal_entry = sg.CalendarButton(
            text,
            close_when_date_chosen=True,
            target=key,
            no_titlebar=False,
            format="%d-%m-%Y",
        )
        return label, entry, cal_entry

    @staticmethod
    def create_combobox(text, key=None, items=None, default_item=None):
        if key is None:
            key = f"-{text.strip().replace(' ', '_').upper()}-"
        if items is None:
            items = []

        label = sg.Text(text, size=(Window.LABEL_SPACING, 1))
        entry = sg.Combo(values=items, default_value=default_item, readonly=True)
        return label, entry

    @staticmethod
    def create_time_selector(text, keys=None, active_selection=None):
        if keys is None:
            keys = [
                f"-{text.strip().replace(' ', '_').upper()}_H-",
                f"-{text.strip().replace(' ', '_').upper()}_M-",
                f"-{text.strip().replace(' ', '_').upper()}_PMAM-",
            ]
        if active_selection is None:
            active_selection = [True] * 3
        elif isinstance(active_selection, dict):
            h = active_selection.get("h", False) or active_selection.get("hour", False)
            m = active_selection.get("m", False) or active_selection.get(
                "minute", False
            )
            pmam = active_selection.get("pmam", False)
            active_selection = [h, m, pmam]

        label = sg.Text(text, size=(Window.LABEL_SPACING, 1))

        get_values = lambda a, b: [str(x).zfill(2) for x in range(a, b + 1)]
        e = []
        if active_selection[0]:
            e.append(sg.Spin(get_values(1, 12), size=(4, 1), pad=(5, 2), key=keys[0]))
        if active_selection[1]:
            e.append(sg.Spin(get_values(0, 59), size=(4, 1), pad=(5, 2), key=keys[1]))
        if active_selection[2]:
            e.append(sg.Spin(["AM", "PM"], size=(4, 1), pad=(5, 2), key=keys[2]))
        return label, *e


if __name__ == "__main__":
    window = Window("Scheduler")

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "-CANCEL-":
            break

        if event == "-CONFIRM-":
            print(values)

    window.close()

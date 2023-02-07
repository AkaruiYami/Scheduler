import PySimpleGUI as sg

from models import model


class TimetableWindow(sg.Window):
    def __init__(self, title, **kwargs):
        self.headers = ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.data = model.Table(self.headers)
        self.cell_size = (20, 1)
        self.data.extend(self.headers[1:], [["A"] * 8] * len(self.headers[1:]))
        self.data["Time"] = ["1:00:00"] * 8
        layout = self._create_layout()
        super().__init__(title, layout, **kwargs)

    def _create_layout(self):
        layout = []
        header_row = [
            sg.Text(
                header,
                relief=sg.RELIEF_RIDGE,
                size=self.cell_size,
                justification="center",
            )
            for header in self.data.keys()
        ]
        data_row = [
            [
                sg.Text(
                    data,
                    size=self.cell_size,
                    justification="center",
                    relief=sg.RELIEF_SUNKEN,
                )
                for data in row
            ]
            for row in self.data.t_values()
        ]

        layout.append(header_row)
        layout.extend(data_row)
        return layout


if __name__ == "__main__":
    window = TimetableWindow("Timetable View")
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == "-TABLE-":
            print(event)
            print(values)

    window.close()

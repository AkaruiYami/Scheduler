import PySimpleGUI as sg

from models import model


class TimetableWindow(sg.Window):
    def __init__(self, title, **kwargs):
        self.headers = ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.data = model.Table(self.headers)
        self.cell_size = (20, 1)
        self.data.extend(self.headers[1:], [["A"] * 8] * len(self.headers[1:]))
        self.data["Time"] = "1:00:00"
        self.data["Monday"][1] = ""
        self.data.update("Tuesday", [""] * 3)
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
        cell_color = lambda x: "#ff0a0a" if x != "" else None
        data_row = [
            [
                self._create_cell(data, cell_color(data))
                for data in row
            ]
            for row in self.data.t_values()
        ]

        layout.append(header_row)
        layout.extend(data_row)
        return layout

    def _create_cell(self, data, color=None):
        return sg.Text(data,
                       size=(self.cell_size[0], 3),
                       relief=sg.RELIEF_SUNKEN,
                       background_color=color,
                       expand_x=True, expand_y=True
                    ) 



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

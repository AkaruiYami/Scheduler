import PySimpleGUI as sg
from datetime import datetime, timedelta


class Cell(sg.Frame):
    TIME_FORMAT = "%I:%M%p"

    def __init__(
        self,
        title,
        *,
        start_time=None,
        description=None,
        text_pad=(5, 3),
        hours=0,
        minutes=0,
        **kwargs,
    ):
        self.title = title

        if start_time is not None:
            self.start_time = datetime.strptime(start_time, self.TIME_FORMAT)
        else:
            self.start_time = start_time

        if hours != 0 or minutes != 0:
            assert start_time is not None, "Missing duration"
            self.duration = timedelta(minutes=minutes, hours=hours)
        else:
            assert start_time is None, "Missing start_time"
            self.duration = None

        if description is not None:
            self.desc = sg.Text(description or "-", size=25, pad=self.TEXT_PADDING)
        else:
            self.desc = "-"

        self.text_padding = text_pad
        self.description = self.desc

        layout = [[ele] for ele in self._create_elements()]
        super().__init__("", layout=layout, **kwargs)

    def _create_elements(self):
        _time = ""
        _duration = ""
        if self.start_time and self.duration:
            _start_time = self.start_time.strftime(self.TIME_FORMAT)
            _end_time = (self.start_time + self.duration).strftime(self.TIME_FORMAT)
            _time = f"{_start_time} - {_end_time}"
            _duration = str(self.duration)

        _title = sg.Text(self.title, pad=self.text_padding)
        _time = sg.Text(_time, pad=self.text_padding)
        _duration = sg.Text(_duration, pad=self.text_padding)
        _desc = sg.Text(self.desc, pad=self.text_padding)

        return _title, _time, _duration, _desc


class TimetableWindow(sg.Window):
    HEADERS = [
        "Time",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    def __init__(self, title="Scheduler"):
        super().__init__(title, self._create_timetable())

    def _create_timetable(self):
        _size = (len(max(self.HEADERS, key=len)) + 5, 1)

        layout = [
            [
                sg.Text(
                    header,
                    size=_size,
                    pad=(5, 0),
                    justification="center",
                    relief=sg.RELIEF_RAISED,
                    expand_x=True,
                )
                for header in self.HEADERS
            ]
        ]
        n = len(self.HEADERS)
        data = [
            [
                Cell(f"Cell {i}", start_time="01:30PM", minutes=120, text_pad=(5, 0))
                for i in range(n)
            ]
            for _ in range(3)
        ]

        layout.extend(data)
        return layout


if __name__ == "__main__":
    window = TimetableWindow()
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

    window.close()

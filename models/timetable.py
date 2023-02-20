import datetime
import PySimpleGUI as sg


class Timetable:
    def __init__(
        self,
        start_time: str,
        end_time: str,
        duration: int,
        time_format: str = "%I:%M%p",
        days: list[str] = None,
    ):
        """Create a table class that hold the timetable data.

        table = {day: {time: content}}

        Args:
            start_time (str): Start time in the format specified in time_format parameter.
            end_time (str): Ending time in the format specified in time_format parameter.
            duration (int): Minutes between each time interval.
            time_format (str, optional): Time format to which the time string is stored and displayed. Defaults to "%I:%M%p".
            days (list[str], optional): A list of days name. Defaults to Monday to Friday.
        """
        if days is None:
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.days = days
        self.start_time = datetime.datetime.strptime(start_time, time_format)
        self.end_time = datetime.datetime.strptime(end_time, time_format)
        self.duration = datetime.timedelta(minutes=duration)
        self.interval = (self.end_time - self.start_time) // self.duration + 1
        self.time_format = time_format
        self.time_frame = [
            (self.start_time + (self.duration * i)).strftime(self.time_format)
            for i in range(self.interval)
        ]
        self.__table = {}
        self._init_empty_table()

    def update_content(self, day: str, time: str, content: str, color: str):
        """Update Content for the spicified day and time.

        Args:
            day (str): The day name string such as "Monday".
            time (str): Time string that has the same format as the the one shown in the timetable. Can use self.time_format to see the format. Default format is "%I:%M%p".
            content (str): The actual content will be put into the sg.Text object in the timetable.
        """
        assert day in self.days, f"{day} is not a valid day"
        assert time in self.time_frame, f"{time} is not a valid time"
        self.__table[day][time].update(content, background_color=color)

    def _init_empty_table(self):
        for day in self.days:
            _column = {
                t: sg.Text("", relief=sg.RELIEF_SUNKEN, expand_x=True, size=(15, 3))
                for t in self.time_frame
            }
            self.__table[day] = _column

    def __getitem__(self, key):
        if isinstance(key, tuple):
            if key[0] in self.days:
                kday, ktime = key
            else:
                ktime, kday = key
            return self.__table[kday][ktime]
        if key in self.time_frame:
            return {day: content[key] for day, content in self.__table.items()}
        return {time: content for time, content in self.__table[key].items()}

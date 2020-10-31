class Person:

    def __init__(self, name, last_name, work_start="", work_end="", meetings=""):
        self.name = name
        self.last_name = last_name
        self.work_start = work_start
        self.work_end = work_end
        self.calendar = list()
        self.parse_calendar(meetings)

    @property
    def email(self):
        return f"{self.name}.{self.last_name}@email.com"

    def __repr__(self):
        return f"Person({self.name}, {self.last_name})"

    def __str__(self):
        return f"{self.name} {self.last_name} is working {self.work_start} - {self.work_end}. Calendar meetings for " \
               f"today: {self.meetings_to_str()} "

    def meetings_to_str(self):
        return ", ".join(f"{meet[0]}-{meet[1]}" for meet in self.calendar)

    def __add__(self, other):
        return Person(f"{self.name} {other.name}", self.last_name)

    def add_calendar_entry(self, meet_text):
        start, end = meet_text.split("-")
        self.calendar.append([start.strip(), end.strip()])

    def parse_calendar(self, cal_times):
        self.calendar = list()
        for cal_entry in cal_times.split(","):
            self.add_calendar_entry(cal_entry)

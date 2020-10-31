import datetime

class Meeting:
    total_time = 0
    date = datetime.datetime.now()

    def __init__(self, name, start_time, end_time, color):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.color = color

    @property
    def time_duration(self):
        if self.end_time < self.start_time:
            raise ValueError('End Time should  not be before Start time.')
        return self.end_time - self.start_time

    def get_time_of_task(self):
        self.total_time = self.end_time - self.start_time

    def __str__(self):
        return f"{self.name} [START]{self.start_time} [END]{self.end_time}"

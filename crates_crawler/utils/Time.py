from datetime import datetime, timedelta
from time import time
from math import ceil


class Time:
    def __init__(self):
        self._start_time = None
        self._result = None

    def start(self):
        self._start_time = time()
        self._result = None
        return self

    def end(self):
        self._result = time() - self._start_time
        self._start_time = None
        return self

    @property
    def result(self):
        return self._result

    @staticmethod
    def now():
        now = datetime.now()
        formatted = now.strftime("%d.%m.%Y %H:%M")
        return formatted

    @staticmethod
    def now_with_seconds():
        now = datetime.now()
        formatted = now.strftime("%d.%m.%Y %H:%M:%S")
        return formatted

    @staticmethod
    def timestamp(date_string):
        datetime_object = datetime.strptime(date_string, '%d.%m.%Y %H:%M')
        return datetime_object.timestamp()

    @staticmethod
    def next(dt, interval):
        secs = dt.minute * 60 + dt.second + dt.microsecond * 1e-6
        delta = ceil(secs / interval) * interval - secs
        return dt + timedelta(seconds=delta)

    @staticmethod
    def timeout(interval):
        now = datetime.now()
        next_time = Time.next(now, interval)
        diff = next_time - now
        return diff.seconds

    @staticmethod
    def backup():
        now = datetime.now()
        return now.strftime("%Y_%m_%d")

    def __str__(self):
        if self._start_time is not None:
            return f"<Time current: {(time() - self._start_time):0.5f}>"
        else:
            return f"<Time result: {self.result:0.5f}>"

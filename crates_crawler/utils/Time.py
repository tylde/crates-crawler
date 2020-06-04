from datetime import datetime
from time import time


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

    def __str__(self):
        if self._start_time is not None:
            return f"<Time current: {(time() - self._start_time):0.5f}>"
        else:
            return f"<Time result: {self.result:0.5f}>"

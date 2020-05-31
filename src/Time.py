from datetime import datetime


class Time:
    @staticmethod
    def now():
        now = datetime.now()
        formatted = now.strftime("%d.%m.%Y %H:%M")
        return formatted

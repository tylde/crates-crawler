import os
import time

from crates_crawler.utils.Time import Time


def main_loop():
    while 1:
        print(Time.now_with_seconds())
        os.system("python main.py")
        next_interval = Time.timeout(600)
        time.sleep(next_interval + 1)


main_loop()

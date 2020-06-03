from src.CratesCrawler import CratesCrawler
from config.crates_set import crates_set

from config.index import LOCAL_API, STEAM_API, OUTPUT
from src.Time import Time

stopper = Time()

stopper.start()

crawler = CratesCrawler(STEAM_API, crates_set, OUTPUT)
crawler.get_data()

stopper.end()

print(f"Program execution time: ({stopper.result:0.3f}s)")


from config.crates_set import crates_set
from config.index import STEAM_API, OUTPUT_DIR, OUTPUT_FILENAME, OUTPUT_FILE_EXTENSION
from crates_crawler.CratesCrawler import CratesCrawler
from crates_crawler.utils.Time import Time

stopper = Time()

stopper.start()

crawler = CratesCrawler(STEAM_API, crates_set, OUTPUT_DIR, OUTPUT_FILENAME, OUTPUT_FILE_EXTENSION)
crawler.get_data()

stopper.end()

print(f"Program execution time: ({stopper.result:0.3f}s)")

from config.contants import STEAM_API
from config.crates_required import REQUIRED_CASED
from config.index import OUTPUT_DIR, OUTPUT_FILENAME, OUTPUT_FILE_EXTENSION
from crates_crawler.CratesCrawler import CratesCrawler
from crates_crawler.utils.Time import Time

stopper = Time()

stopper.start()

crawler = CratesCrawler(STEAM_API, REQUIRED_CASED, OUTPUT_DIR, OUTPUT_FILENAME, OUTPUT_FILE_EXTENSION)
crawler.get_data()

stopper.end()

print(f"Program execution time: ({stopper.result:0.3f}s)")

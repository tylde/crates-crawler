from src.CratesCrawler import CratesCrawler
from config.crates_set import crates_set

from config.index import LOCAL_API, STEAM_API, OUTPUT


crawler = CratesCrawler(LOCAL_API, crates_set, OUTPUT)
crawler.get_data()
print('END')

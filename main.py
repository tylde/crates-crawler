from src.CratesCrawler import CratesCrawler
from config.crates_set import crates_set

crawler = CratesCrawler(crates_set)
crawler.get_data()

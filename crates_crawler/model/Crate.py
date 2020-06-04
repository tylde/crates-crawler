from config.contants import CRATE_SUFFIX
from config.crates_dictonary import crates_dictonary


class Crate:
    def __init__(self, crate_name):
        self.id = crates_dictonary.get(crate_name + CRATE_SUFFIX.get('ID_SUFFIX'))
        self.name = crates_dictonary.get(crate_name + CRATE_SUFFIX.get('NAME_SUFFIX'))
        self.short_name = crates_dictonary.get(crate_name + CRATE_SUFFIX.get('SHORT_NAME_SUFFIX'))
        self.histogram_id = crates_dictonary.get(crate_name + CRATE_SUFFIX.get('HISTOGRAM_ID_SUFFIX'))
        self.price_overview_name = crates_dictonary.get(crate_name + CRATE_SUFFIX.get('PRICE_OVERVIEW_SUFFIX'))

    def __str__(self):
        return '<Crate \"' + str(self.short_name) + '\">'

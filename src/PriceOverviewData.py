class PriceOverviewData:
    def __init__(self, status: bool, volume: str, lowest_price: str, median_price: str):
        self.status = status
        self.volume = int(volume.replace(',', ''))
        self.lowest_price = lowest_price
        self.median_price = median_price

    @classmethod
    def from_response(cls, response):
        if response is None:
            return cls(False, '0', '', '')
        return cls(True, response['volume'], response['lowest_price'], response['median_price'])

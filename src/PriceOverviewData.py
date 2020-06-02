class PriceOverviewData:
    def __init__(self, volume: str, lowest_price: str, median_price: str):
        self.volume = int(volume.replace(',', ''))
        self.lowest_price = lowest_price
        self.median_price = median_price

    @classmethod
    def from_response(cls, response):
        return cls(response['volume'], response['lowest_price'], response['median_price'])

import re

from config.contants import SUMMARY_REGEX


class OrdersHistogramData:
    def __init__(self, status: bool, sell_orders: int, buy_orders: int, sell_order_list, buy_order_list, price):
        self.status = status
        self.sell_orders = sell_orders
        self.buy_orders = buy_orders
        self.sell_order_list = sell_order_list
        self.buy_order_list = buy_order_list
        self.price = price

    @classmethod
    def from_response(cls, response):
        if response is None:
            return cls(False, 0, 0, [], [], '')

        buy_orders = OrdersHistogramData.parse_summary(response['buy_order_summary'])
        sell_orders = OrdersHistogramData.parse_summary(response['sell_order_summary'])
        sell_order_list = OrdersHistogramData.parse_order_graph(response['sell_order_graph'])
        buy_order_list = OrdersHistogramData.parse_order_graph(response['buy_order_graph'])
        price = OrdersHistogramData.get_price_from_sell_orders(sell_order_list)
        return cls(True, sell_orders, buy_orders, sell_order_list, buy_order_list, price)

    @staticmethod
    def parse_order_graph(order_graph):
        order_list = []
        for i in range(len(order_graph)):
            [price, total, info] = order_graph[i]
            amount: int
            if i == 0:
                amount = total
            else:
                [price_before, total_before, info_before] = order_graph[i - 1]
                amount = total - total_before
            order_list.append([price, amount])

        return order_list

    @staticmethod
    def parse_summary(summary) -> int:
        match = re.search(SUMMARY_REGEX, summary)
        if match is not None:
            return int(match[0])
        return 0

    @staticmethod
    def get_price_from_sell_orders(sell_order_list):
        if len(sell_order_list):
            return sell_order_list[0][0]
        return ''

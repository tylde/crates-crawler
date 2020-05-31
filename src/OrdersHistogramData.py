import re

from config.contants import SUMMARY_REGEX


class OrdersHistogramData:
    def __init__(self, sell_orders: int, buy_orders: int, sell_order_list, buy_order_list):
        self.sell_orders = sell_orders
        self.buy_orders = buy_orders
        self.sell_order_list = sell_order_list
        self.buy_order_list = buy_order_list

    @classmethod
    def from_response(cls, response):
        buy_orders = OrdersHistogramData.parse_summary(response['buy_order_summary'])
        sell_orders = OrdersHistogramData.parse_summary(response['sell_order_summary'])

        sell_order_list = OrdersHistogramData.parse_order_graph(response['sell_order_graph'])
        buy_order_list = OrdersHistogramData.parse_order_graph(response['buy_order_graph'])

        return cls(sell_orders, buy_orders, sell_order_list, buy_order_list)

    @staticmethod
    def parse_order_graph(order_graph):
        order_list = []
        for i in range(len(order_graph)):
            [price, total, info] = order_graph[i]
            amount: int
            if i == 0:
                amount = total
            else:
                [price_last, total_last, info_last] = order_graph[i - 1]
                amount = total - total_last
            order_list.append([price, amount])

        return order_list

    @staticmethod
    def parse_summary(summary) -> int:
        match = re.search(SUMMARY_REGEX, summary)
        if match is not None:
            return int(match[0])
        return 0

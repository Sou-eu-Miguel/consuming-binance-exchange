import numpy
import requests
from sma import Sma


class Binance:
    api_root = "https://api.binance.com/"
    intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']

    def __init__(self, symbol='ETHBTC', interval='1m', limit=200):
        self.symbol = symbol
        self.interval = interval
        self.limit = limit

    def api_url(self, symbol='ETHBTC', interval='1m', limit=200):
        return self.api_root + ('api/v1/klines?symbol={}&interval={}&limit={}').format(symbol, interval, limit)

    def request_api(self, interval):
        response = requests.get(self.api_url(interval=interval, limit=self.limit))
        return response.json()

    def get_closes(self, klines):
        list_closes = []

        for item in klines:
            list_closes.append(float(item[4]))

        return list_closes

    def get_close_all_interval_map(self, intervals=intervals):
        close_map = {}

        for interval in intervals:
            klines = self.request_api(interval)
            close_map[interval] = self.get_closes(klines)

        return close_map

    def get_close_by_interval_map(self, interval):
        return self.get_close_all_interval_map(interval.split())

    def get_sma(self, closes, period=12):
        closes_interval = list(closes.keys())[0]
        closes_values = list(closes.values())[0]

        sma = Sma(closes_interval, period)

        limit_range = len(closes_values) - period
        for i in range(0, limit_range):
            closes_mean = numpy.mean(closes_values[i:(i + period)], dtype=numpy.float)
            sma.values.append(closes_mean)

        return sma


if __name__ == '__main__':
    b = Binance()

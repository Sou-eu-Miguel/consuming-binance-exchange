class Sma:
    def __init__(self, interval, period):
        self.interval = interval
        self.period = period
        self.values = []

    def __str__(self):
        return 'Interval: {} Period: {} values: {}'.format(self.interval, self.period, self.values)

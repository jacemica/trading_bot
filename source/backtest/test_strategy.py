import backtrader as bt
import backtrader.indicators as btind
import math

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        self.stoc = btind.StochasticFast(self.datas[0], period=14, period_dfast=3)
        self.stochfast = self.stoc.percK
        self.stochslow = self.stoc.percD

        self.macd = btind.MACD(self.datas[0])
        self.mfast = self.macd.macd
        self.mslow = self.macd.signal

        self.bb = btind.BBands(self.datas[0])
        self.b = ((self.bb.mid - self.bb.bot) * 0.3) + self.bb.bot

        self.shares = 28

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        if not self.position:
            if self.stochfast <= 25 and self.stochslow <= self.stochfast and self.dataclose <= self.b:
                self.order = self.buy(size = self.shares)
        
        else:
            if (self.stochfast >= 65) and (self.mfast - self.mslow <= -.2):
                self.order = self.sell(size = self.shares)
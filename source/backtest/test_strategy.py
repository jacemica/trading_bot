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

        self.stoc = btind.StochasticFull(self.datas[0])
        self.stochfast = self.stoc.percD
        self.stochslow = self.stoc.percDSlow

        self.macd = btind.MACDHisto(self.datas[0])
        self.macd = self.macd.histo

        self.bb = btind.BBands(self.datas[0])
        self.b = self.bb.top * .99

        self.shares = 1

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])
        if not self.position:
            # if (self.stochslow[-1] <= self.stochfast[-1]) and (self.stochfast[-1] <= 20) and (self.dataclose[0] <= self.b[0]):
            if self.stochfast[-1] <= 20:
                #BLACK STOCHASTIC > RED STOCHASTIC             BLACK STOCHASTIC <= 20         CURRENT PRICE IN LOWER BOLLINGER BAND RANGE
                self.log('buy')
                self.order = self.buy(size = self.shares)

        else:
            # if (self.stochfast[-1] <= self.stochslow[-1]) and (self.stochfast[-1] >= 65) and (self.macd[-1] <= 0.2) and self.dataclose[0] >= self.b[0]:
            if self.dataclose[0] >= self.b[0] and self.macd[-1] <= 0.2:
                #BLACK STOCHASTIC < RED STOCHASTIC             BLACK STOCHASTIC >= 68         MACD NEGATIVE
                self.log('sell')
                self.order = self.sell(size = self.shares)
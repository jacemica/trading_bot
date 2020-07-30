import backtrader as bt
import datetime
from test_strategy import TestStrategy

STOCK = 'INTC'
cerebro = bt.Cerebro()
cerebro.broker.set_cash(5000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
print(STOCK)

data = bt.feeds.YahooFinanceCSVData(
    dataname='source/backtest/Historical_Data/{}.csv'.format(STOCK),

    # Do not pass values before this date
    fromdate=datetime.datetime(2017, 10, 1),
    # Do not pass values after this date
    todate=datetime.datetime(2018, 9, 30),
    reverse=False)

cerebro.adddata(data)

cerebro.addstrategy(TestStrategy)

cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()
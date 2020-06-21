import alpaca_trade_api as tradeapi
import requests, json
from pprint import pprint
from config import * 

BASE_URL = "https://paper-api.alpaca.markets"
STOCKS = ["INTC", "AMD", "NVDA", "IBM", "WDC", "AAPL", "FB", "MSFT", "AMZN", "NFLX", "TWTR", "CRM", "DBX", "WORK", "TWLO", "SQ", "PYPL", "CSCO", "ADBE", "SNE", "NTODY", "LYFT", "UBER", "TSLA", "WFC", "JPM", "BAC", "AXP", "MA", "V", "DIS", "TGT", "WMT", "NKE", "KO", "KHC", "SBUX", "GRUB"]


def moving_average(api, stocks, days):
    for stock in stocks:
        barSum = 0
        ma = api.get_barset(stock, "1D", days)
        barset = ma[stock]
        for bar in barset:
            barSum += bar.c

    return barSum/days

api = tradeapi.REST(API_KEY, SEC_KEY, BASE_URL)
ma_50 = moving_average(api, STOCKS, 50)

print(ma_50)
# barsum = 0
# aapl_barset = barset["AAPL"]
# for bar in aapl_barset:
#     barsum += bar.c

# print(barsum/50)
print("EOF")
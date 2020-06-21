import alpaca_trade_api as tradeapi
import requests, json, statistics
from config import * 

BASE_URL = "https://paper-api.alpaca.markets"
STOCKS = ["INTC", "AMD", "NVDA", "IBM", "WDC", "AAPL", "FB", "MSFT", "AMZN", "NFLX", "TWTR", "CRM", "DBX", "WORK", "TWLO", "SQ", "PYPL", "CSCO", "ADBE", "SNE", "NTODY", "LYFT", "UBER", "TSLA", "WFC", "JPM", "BAC", "AXP", "MA", "V", "DIS", "TGT", "WMT", "NKE", "KO", "KHC", "SBUX", "GRUB"]

def moving_average(api, stock, days):
    barSum = 0
    ma = api.get_barset(stock, "1D", days)
    barset = ma[stock]
    for bar in barset:
        barSum += bar.c

    return barSum/days

def is_golden_cross(api, stock):
    return moving_average(api, stock, 50) > moving_average(api, stock, 200)

def bollinger_bands(api, stock):
    sma = moving_average(api, stock, 20)
    std_dev = standard_deviation(api, stock)
    UBB = sma + (2 * std_dev)
    LBB = sma - (2 * std_dev)

    return (LBB, UBB)

def standard_deviation(api, stock):
    close_list = []

    ma = api.get_barset(stock, "1D", 20)
    barset = ma[stock]
    for bar in barset:
        close_list.append(bar.c)

    return statistics.pstdev(close_list)

def stochastics(api, stock):
    L14 = float('inf')
    H14 = float('-inf')
    L3 = float('inf')
    H3 = float('-inf')

    k_ma = api.get_barset(stock, "1D", 14)
    k_barset = k_ma[stock]

    CP = k_barset[-1].c

    for bar in k_barset:
        if bar.l < L14:
            L14 = bar.l
        if bar.h > H14:
            H14 = bar.h

    slow = 100 * (CP - L14) / (H14 - L14)

if __name__ == "__main__":
    api = tradeapi.REST(API_KEY, SEC_KEY, BASE_URL)
    print(stochastics(api, "MSFT"))
    print("EOF")
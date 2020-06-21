import alpaca_trade_api as tradeapi
from config import * 
from indicators import *

BASE_URL = "https://paper-api.alpaca.markets"
STOCKS = ["INTC", "AMD", "NVDA", "IBM", "WDC", "AAPL", "FB", "MSFT", "AMZN", "NFLX", "TWTR", "CRM", "DBX", "WORK", "TWLO", "SQ", "PYPL", "CSCO", "ADBE", "SNE", "NTODY", "LYFT", "UBER", "TSLA", "WFC", "JPM", "BAC", "AXP", "MA", "V", "DIS", "TGT", "WMT", "NKE", "KO", "KHC", "SBUX", "GRUB"]

if __name__ == "__main__":
    api = tradeapi.REST(API_KEY, SEC_KEY, BASE_URL)
    print("EOF")
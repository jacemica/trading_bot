import alpaca_trade_api as tradeapi
from config import * 
from indicators import *
from helpers import *
import datetime, time, requests

BASE_URL = "https://paper-api.alpaca.markets"
myPicks = ["INTC", "AMD", "NVDA", "IBM", "WDC", "AAPL", "FB", "MSFT", "AMZN", "NFLX", "TWTR", "CRM", "DBX", "WORK", "TWLO", "SQ", "PYPL", "CSCO", "ADBE", "SNE", "NTDOY", "LYFT", "UBER", "TSLA", "WFC", "JPM", "BAC", "AXP", "MA", "V", "DIS", "TGT", "WMT", "NKE", "KO", "KHC", "SBUX", "GRUB"]

if __name__ == "__main__":
    api = tradeapi.REST(API_KEY, SEC_KEY, BASE_URL)
    STOCKS = combine_STOCKS(myPicks, get_SPY())
  
    date = datetime.date.today()
    pre_market = get_open(date)
    print(pre_market)

    while datetime.datetime.now() < pre_market:
        print("Waiting for pre-markets...")
        time.sleep(900)

    if not check_sell(api):
        stocks_dict = find_stocks(api, STOCKS, date)
        print("\nPotential stocks: \n", stocks_dict, '\n')

        check_buy(api, stocks_dict)    
    
    print("Program Terminated")
    sys.exit(0)
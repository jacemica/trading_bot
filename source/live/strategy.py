import alpaca_trade_api as tradeapi
from config import * 
from indicators import *
from helpers import *
import datetime, time, requests

PAPER_BASE_URL = "https://paper-api.alpaca.markets"
LIVE_BASE_URL = "https://api.alpaca.markets"

myPicks = {"TWTR", "DBX", "WORK", "SQ", "SNE", "LYFT", "UBER"}

if __name__ == "__main__":
    paper_api = tradeapi.REST(PAPER_API_KEY, PAPER_SEC_KEY, PAPER_BASE_URL)
    live_api = tradeapi.REST(LIVE_API_KEY, LIVE_SEC_KEY, LIVE_BASE_URL)

    SP = 'https://en.wikipedia.org/wiki/S%26P_100#Components'
    NDX = 'https://en.wikipedia.org/wiki/NASDAQ-100#Components'
    STOCKS = myPicks.union(get_tickers(SP), get_tickers(NDX))

    date = datetime.date.today()
    pre_market = get_open(date)
    print(pre_market)

    # while datetime.datetime.now() < pre_market:
    #     print("Waiting for pre-markets...")
    #     time.sleep(900)
    
    if check_sell(live_api, paper_api) or len([position.symbol for position in live_api.list_positions()]) < 10:
        stocks_dict = find_stocks(live_api, STOCKS) 
        print("\nPotential stocks: \n", stocks_dict, '\n')    

        while len(live_api.list_orders()) > 0:
            print("Cannot buy stocks until sell orders executed")
            time.sleep(300)

        check_buy(live_api, paper_api, stocks_dict)
    
    print("Program Terminated")
    input("Press ENTER to exit:")
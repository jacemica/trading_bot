import alpaca_trade_api as tradeapi
from config import * 
from indicators import *
from helpers import *
import datetime, time, requests

PAPER_BASE_URL = "https://paper-api.alpaca.markets"
LIVE_BASE_URL = "https://api.alpaca.markets"
STOCKS = ['ADBE', 'AMD', 'GOOGL', 'GOOG', 'AMZN', 'AAPL', 'ADSK', 'AVGO', \
            'CSCO', 'CTXS', 'CMCSA', 'COST', 'DOCU', 'EBAY', 'EA', 'FB', \
            'FISV', 'INTC', 'INTU', 'ISRG', 'KHC', 'MXIM', 'MCHP', 'MU', \
            'MSFT', 'NFLX', 'NVDA', 'PYPL', 'PEP', 'QCOM', 'SWKS', 'SPLK', \
            'SBUX', 'SNPS', 'TMUS', 'TTWO', 'TSLA', 'TXN', 'VRSN', 'WDAY', \
            'WDC', 'XLNX', 'ZM', 'CRM', 'V', 'MA', 'AXP', 'BAC', 'DIS', \
            'IBM', 'JNJ', 'JPM', 'KO', 'MCD', 'ORCL', 'TGT', 'TWTR', 'DBX', \
            'WORK', 'SQ', 'SNE', 'LYFT', 'UBER', 'TWLO', 'ROKU', 'Z', 'DELL', \
            'TXN', 'QRVO', 'GLW', 'ASML', 'TSM', 'APD', 'A', 'KLAC', 'WMT', \
            'MCO', 'CHTR', 'MRVL']

if __name__ == "__main__":
    live_api = tradeapi.REST(LIVE_API_KEY, LIVE_SEC_KEY, LIVE_BASE_URL)
    print("\nCurrent cash available:", live_api.get_account().cash) 

    cooldown()

    date = datetime.date.today()
    pre_market = get_open(date)
    print(pre_market)

    while datetime.datetime.now() < pre_market:
        print("Waiting for pre-markets...")
        time.sleep(900)
    
    if check_sell(live_api) or len([position.symbol for position in live_api.list_positions()]) < 5:
        stocks_dict = find_stocks(live_api, STOCKS) 
        print("\nPotential stocks: \n", stocks_dict, '\n')    

        while len([order.symbol for order in live_api.list_orders() if order.order_type != 'trailing_stop']) > 0:
            print("Cannot buy stocks until sell orders executed")
            time.sleep(300)

        check_buy(live_api, stocks_dict)

    print("\nCurrent cash available:", live_api.get_account().cash)  
    print("Program Terminated")
    input("Press ENTER to exit:")
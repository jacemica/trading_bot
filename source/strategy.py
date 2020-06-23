import alpaca_trade_api as tradeapi
from config import * 
from indicators import *
import datetime, time, math

BASE_URL = "https://paper-api.alpaca.markets"
STOCKS = ["INTC", "AMD", "NVDA", "IBM", "WDC", "AAPL", "FB", "MSFT", "AMZN", "NFLX", "TWTR", "CRM", "DBX", "WORK", "TWLO", "SQ", "PYPL", "CSCO", "ADBE", "SNE", "NTDOY", "LYFT", "UBER", "TSLA", "WFC", "JPM", "BAC", "AXP", "MA", "V", "DIS", "TGT", "WMT", "NKE", "KO", "KHC", "SBUX", "GRUB"]

def find_stocks(api, STOCKS, date_object):
    potential_buys = {}
    counter = 0  
   
    for stock in STOCKS:
        if counter < 5:
            print("Analyzing " + stock)
            counter += 1
            gc = is_golden_cross(api, stock)
            bb = bollinger_bands(api, stock)
            st = av_stochastics(AV_KEY, stock, str(date_object)) 
            st_fast = float(st['SlowK'])
            st_slow = float(st['SlowD'])
            ma = api.get_barset(stock, "1D", 1)[stock]
            price = ma[0].c
            b = ((bb[1] - bb[0]) * 0.33) + bb[0]

            if (gc) and (price > bb[0] and price < b) and (st_fast > st_slow) & (st_fast < 25):
                print(stock + " shows potential!")
                potential_buys[st_fast] = (stock, price)

        else:
            print("API Cooldown for 1 Minute")
            for i in range(60,0,-1):
                time.sleep(1)
                print(i)
                counter = 0
    
    return potential_buys

if __name__ == "__main__":
    date_object = datetime.date.today()
    api = tradeapi.REST(API_KEY, SEC_KEY, BASE_URL)
    account = api.get_account()
    capital = account.buying_power
    pre_market = datetime.datetime(2020, 6, 23, 5, 30)

    while datetime.datetime.now() < pre_market:
        print("Waiting for pre-markets...")
        time.sleep(900)

    stocks_dict = find_stocks(api, STOCKS, date_object)
    if len(stocks_dict) != 0:
        try:
            for stock in sorted(stocks_dict):
                symbol = stocks_dict[stock][0]
                side = 'buy'
                t = 'limit'
                tif = 'day'
                qty = math.floor(capital / 3.33 / stocks_dict[stock][-1])
                limit_price = stocks_dict[stock][-1] + 5

                order = api.submit_order(symbol, qty, side, t, tif, limit_price)
                print(str(qty) + " shares of " + symbol + " purchased!")
                print(order)

        except Exception as e:
            print("COULD NOT SUBMIT ORDER")
            print(e)
    else:
        print("No stocks fit criteria")

    print("Program Terminated")
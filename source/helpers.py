import time, datetime, pickle, requests, bs4, math
from config import *
from indicators import *
from pandas_datareader import data
from collections import OrderedDict 

def check_buy(api, stocks_dict):
    capital = api.get_account().cash
    positions = [position.symbol for position in api.list_positions()]
    orders = [order.symbol for order in api.list_orders()]

    if (len(stocks_dict) != 0) and (len(positions) < 10):
        try:
            for stock in stocks_dict:
                symbol = stocks_dict[stock][0]
                qty = int((math.floor(float(capital)) / (10-len(positions)) / (stocks_dict[stock][-1])))
                
                limit_price = stocks_dict[stock][-1] + 2

                if ((len(api.list_positions()) + len(api.list_orders())) < 10) and ((symbol not in positions) and (symbol not in orders)):
                    order = api.submit_order(symbol=symbol, qty=qty, side='buy', type='limit', time_in_force='day', limit_price=limit_price, extended_hours=True)
                    print(order, '\n')
                    print(str(qty) + " shares of " + str(symbol) + " purchased!")

                else:
                    print("DID NOT SUBMIT ORDER - PORTFOLIO FULL/ALREADY OWNED")

        except Exception as e:
            print("COULD NOT SUBMIT ORDER")
            print(e)
    else:
        print("No stocks fit criteria/Portfolio Full")

def check_sell(api):
    sell_flag = 0
    print("Checking for positions to sell")
    positions = api.list_positions()

    for position in positions:
        print("Analyzing " + str(position.symbol))
        st = av_stochastics(AV_KEY, position.symbol)
        st_fast = float(st['SlowK'])
        st_slow = float(st['SlowD'])
        MACD = float(macd(AV_KEY, position.symbol))

        if ((st_fast>75) and (st_fast<st_slow)) or ((st_fast>70) and (MACD<=0)):
            sell_flag = 1
            print("Selling position: " + position.symbol)
            order = api.submit_order(symbol=position.symbol, qty=position.qty, side="sell", type="limit", time_in_force="day", limit_price=float(position.current_price)-2, extended_hours=True)
            print(order)

        print("API Cooldown for 1 Minute")
        for i in range(60,0,-1):
                time.sleep(1)

    if sell_flag == 0:
        print("No positions to sell at this time")

def find_stocks(api, STOCKS, date_object):
    potential_buys = {}

    for idx, stock in enumerate(STOCKS):
        try:
            if idx%5==0 and idx>0:
                print("API Cooldown for 1 Minute")
                for i in range(60,0,-1):
                    time.sleep(1)

            print("Analyzing " + stock + " " + str(idx+1) + " of " + str(len(STOCKS)))

            gc = is_golden_cross(api, stock)
            bb = bollinger_bands(api, stock)
            b = ((bb[1] - bb[0]) * 0.33) + bb[0]

            st = av_stochastics(AV_KEY, stock) 
            st_fast = float(st['SlowK'])
            st_slow = float(st['SlowD'])

            ma = api.get_barset(stock, "1D", 1)[stock]
            price = ma[0].c
            marketCap = data.get_quote_yahoo(stock)['marketCap'][-1]

            if ((gc) and (st_fast<20)) or ((price<b) and (st_fast<20)):
                print(stock + " shows potential!")
                potential_buys[marketCap] = (stock, price)

        except Exception as e:
            print("API Error")
            print(e)
    
    return OrderedDict(sorted(potential_buys.items(), reverse=True)) 

def get_SPY():
    resp = requests.get('https://en.wikipedia.org/wiki/S%26P_100#Components')
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers   

def combine_STOCKS(STOCKS, SPY):
    for stock in SPY:
        if stock[:-1] not in STOCKS:
            STOCKS.append(stock[:-1]) 

    return STOCKS

def get_open(date):
    Y = int(date.strftime("%Y"))
    M = int(date.strftime("%m"))
    D = int(date.strftime("%d"))

    if datetime.datetime.now() < datetime.datetime(Y, M, D, 5):
        print("Executed morning of")
        pre_market = datetime.datetime(Y, M, D, 5)
    else:
        print("Executed night before")
        pre_market = datetime.datetime(Y, M, D, 5) + datetime.timedelta(days=1)

    return pre_market
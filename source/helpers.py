import time, datetime, pickle, requests, bs4, math
from config import *
from indicators import *

def check_buy(api, stocks_dict):
    capital = api.get_account().buying_power
    positions = [position.symbol for position in api.list_positions()]

    if len(stocks_dict) != 0:
        try:
            for stock in sorted(stocks_dict):
                symbol = stocks_dict[stock][0]
                side = 'buy'
                t = 'limit'
                tif = 'day'
                qty = math.floor(float(capital) / 10 / stocks_dict[stock][-1])
                
                limit_price = stocks_dict[stock][-1] + 2

                if (len(api.list_positions()) < 10) and (symbol not in positions):
                    order = api.submit_order(symbol, qty, side, t, tif, limit_price)
                    print(order, '\n')
                    print(str(qty) + " shares of " + str(symbol) + " purchased!")

                else:
                    print("DID NOT SUBMIT ORDER - PORTFOLIO FULL\ALREADY OWNED")

        except Exception as e:
            print("COULD NOT SUBMIT ORDER")
            print(e)
    else:
        print("No stocks fit criteria")

def check_sell(api):
    print("Checking for positions to sell")
    positions = api.list_positions()

    for position in positions:
        st = av_stochastics(AV_KEY, position.symbol)
        st_fast = float(st['SlowK'])
        MACD = macd(AV_KEY, position.symbol)

        if (st_fast > 70) and (MACD < 0):
            print("Selling position: " + position.symbol)
            order = api.submit_order(symbol=position.symbol, qty=position.qty, side="sell", type="limit", time_in_force="day", limit_price=float(position.current_price)-2)
            print(order)

        print("API Cooldown for 1 Minute")
        for i in range(60,0,-1):
                time.sleep(1)

def find_stocks(api, STOCKS, date_object):
    potential_buys = {}
    counter = 0  
   
    for idx, stock in enumerate(STOCKS):
        if counter < 5:
            print("Analyzing " + stock + " " + str(idx+1) + " of " + str(len(STOCKS)))
            counter += 1
            gc = is_golden_cross(api, stock)
            bb = bollinger_bands(api, stock)
            st = av_stochastics(AV_KEY, stock) 
            st_fast = float(st['SlowK'])
            st_slow = float(st['SlowD'])
            ma = api.get_barset(stock, "1D", 1)[stock]
            price = ma[0].c
            b = ((bb[1] - bb[0]) * 0.33) + bb[0]

            if (price < b) and (st_fast < 25):
                print(stock + " shows potential!")
                potential_buys[st_fast] = (stock, price)

        elif idx+1 != len(STOCKS):
            print("API Cooldown for 1 Minute")
            for i in range(60,0,-1):
                time.sleep(1)
                counter = 0
    
    return potential_buys

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

    print("Executed night before")
    pre_market = datetime.datetime(Y, M, D, 5) + datetime.timedelta(days=1)

    return pre_market
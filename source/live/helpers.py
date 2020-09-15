import time, datetime, pickle, requests, bs4, math, os
from config import *
from indicators import *
from pandas_datareader import data
from collections import OrderedDict 

def check_buy(live_api, stocks_dict):
    r = open("./source/live/cooldown.txt", "r")
    cooldown = r.readlines()
    
    capital = live_api.get_account().cash
    positions = [position.symbol for position in live_api.list_positions()]
    orders = [order.symbol for order in live_api.list_orders()]

    if (len(stocks_dict) != 0) and (len(positions) < 5):
        for stock in stocks_dict:
            try:
                symbol = stocks_dict[stock][0]
                qty = int((math.floor(float(capital)) / (5-len(positions)) / (stocks_dict[stock][-1])))  
                limit_price = stocks_dict[stock][-1] + (stocks_dict[stock][-1] * 0.025)

                for block in cooldown:
                    if symbol in block:
                        raise Exception(symbol + " ON COOLDOWN")
                        
                if ((len(live_api.list_positions()) + len(live_api.list_orders())) < 5) and ((symbol not in positions) and (symbol not in orders)):
                    live_api.submit_order(symbol=symbol, qty=qty, side='buy', type='limit', time_in_force='day', limit_price=limit_price)
                    print(str(qty) + " shares of " + str(symbol) + " purchased at limit: $" + str(limit_price))

                else:
                    raise Exception(symbol + " ALREADY OWNED/PORTFOLIO FULL")

            except Exception as e:
                print("DID NOT SUBMIT ORDER -", e)

    else:
        print("No stocks fit criteria/Portfolio Full")
    
    r.close()

def check_sell(live_api):
    sell_flag = 0
    print("Checking for positions to sell")
    positions = live_api.list_positions()

    for position in positions:
        try:
            print("Analyzing " + str(position.symbol))

            technical_indicator = REDACTED
            technical_indicator = REDACTED
            technical_indicator = REDACTED
            technical_indicator = REDACTED

            price = float(position.current_price)
            entry = float(position.avg_entry_price)
            limit_price = float(price*0.975)

            if (price >= (entry * 1.04)):
                print("GAINED 5%, TRAILING STOP")       #SAVING PROFITS
                print("Trailing position: " + position.symbol)

                live_api.submit_order(symbol=position.symbol, qty=position.qty, side="sell", type="trailing_stop", time_in_force="gtc", trail_percent=2)

            if (price <= (entry * 0.95)):               #EMERGENCY EXIT STRATEGY
                sell_flag = 1
                print("LOST 5%, AUTOMATIC SELL")
                print("Selling position: " + position.symbol)
                
                live_api.submit_order(symbol=position.symbol, qty=position.qty, side="sell", type="limit", time_in_force="day", limit_price=limit_price)
                print(str(position.qty) + " shares of " + str(position.symbol) + " purchased at limit: $" + str(limit_price)) 
                
                w = open("./source/live/cooldown.txt", "a")
                w.write(position.symbol + ',' + datetime.datetime.now().strftime("%Y-%m-%d") + ',' + '\n')
                w.close()

            if (technical_indicator) and (technical_indicator):
                print(price, b)
                sell_flag = 1
                print("Selling position: " + position.symbol)

                live_api.submit_order(symbol=position.symbol, qty=position.qty, side="sell", type="limit", time_in_force="day", limit_price=limit_price)

            print("API Cooldown for 1 Minute")
            for i in range(65,0,-1):
                    time.sleep(1)

        except Exception as e:
            print("SELL FAILED")
            print(e)

    if not sell_flag:
        print("No positions to sell at this time")

    return sell_flag

def find_stocks(live_api, STOCKS):
    potential_buys = {}

    for idx, stock in enumerate(STOCKS):
        stock = stock.rstrip()
        try:
            if idx%5==0 and idx>0:
                print("API Cooldown for 1 Minute")
                for i in range(65,0,-1):
                    time.sleep(1)

            print("Analyzing " + stock + " " + str(idx+1) + " of " + str(len(STOCKS)))
            
            technical_indicator = REDACTED
            technical_indicator = REDACTED
            technical_indicator = REDACTED

            technical_indicator = REDACTED
            technical_indicator = REDACTED
            technical_indicator = REDACTED
            
            technical_indicator = REDACTED
            technical_indicator = REDACTED
            technical_indicator = REDACTED

            price = float(live_api.get_barset(stock, "1D", 1)[stock][0].c)
            marketCap = data.get_quote_yahoo(stock)['marketCap'][-1]

            if (technical_indicator) and (technical_indicator) and (technical_indicator):
                print(stock + " shows potential!")
                potential_buys[marketCap] = (stock, price)

        except Exception as e:
            print("API Error")
            print(e)
    
    return OrderedDict(sorted(potential_buys.items(), reverse=True)) 

def get_tickers(components):
    col = 1 if 'NASDAQ' in components else 0
    resp = requests.get(components)
    soup = bs4.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable', 'id': 'constituents'})
    tickers = set()
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[col].text
        tickers.add(ticker)
        
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        
    return tickers   

def get_open(date):
    Y = int(date.strftime("%Y"))
    M = int(date.strftime("%m"))
    D = int(date.strftime("%d"))

    if datetime.datetime.now() < datetime.datetime(Y, M, D, 5):
        pre_market = datetime.datetime(Y, M, D, 5)
    else:
        pre_market = datetime.datetime(Y, M, D, 5) + datetime.timedelta(days=1)

    return pre_market

def cooldown():
    try:
        os.chdir(r'C:\Users\Jace\Documents\Projects\trading_bot')
        r = open("./source/live/cooldown.txt", "r")
        cooldown = r.readlines()
        rewrites = ['\n']
        today = datetime.datetime.now()

        for block in cooldown[1:]:
            item = block.split(',')
            date = item[1]
            date = datetime.datetime.strptime(date, "%Y-%m-%d")

            if today >= date + datetime.timedelta(days=7):
                print("COOLDOWN COMPLETE, REMOVING", item[0], "FROM COOLDOWN LIST")
                rewrites.append(block)

                w = open("./source/live/cooldown.txt", "a")
                w.truncate(0)
                
                rewrites = list(set(rewrites)-set(cooldown))

                for line in rewrites:
                    w.write(line)

                w.close()
        
        r.close()
    
    except Exception as e:
        print(e)

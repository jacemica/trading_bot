import statistics, json, urllib.request, urllib.parse

def moving_average(api, stock, days):
    barSum = 0
    ma = api.get_barset(stock, "1D", days)
    barset = ma[stock]
    for bar in barset:
        barSum += bar.c

    return barSum/days

def is_golden_cross(api, stock):
    return 0 < (moving_average(api, stock, 50)-moving_average(api, stock, 200)) < 3

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

def av_stochastics(av_key, stock):
    URL = "https://www.alphavantage.co/query?function=STOCH&symbol={}&interval=daily&fastkperiod=14&apikey={}".format(stock, av_key)
    response = urllib.request.urlopen(URL)
    json_text = response.read().decode(encoding = 'utf-8')
    response.close()

    date = list(json.loads(json_text)["Technical Analysis: STOCH"].keys())[0] 
    try:
        return json.loads(json_text)["Technical Analysis: STOCH"][date]
    except Exception as e:
        print("Error: " , e)
        return {'SlowK':99, 'SlowD':99}

def macd(av_key, stock):
    URL = "https://www.alphavantage.co/query?function=MACD&symbol={}&interval=daily&series_type=close&apikey={}".format(stock, av_key)
    response = urllib.request.urlopen(URL)
    json_text = response.read().decode(encoding = 'utf-8')
    response.close()
    
    date = list(json.loads(json_text)["Technical Analysis: MACD"].keys())[0] 
    try:
        return json.loads(json_text)["Technical Analysis: MACD"][date]["MACD_Hist"]
    except Exception as e:
        print("Error: ", e)
        return 0
    
    
    

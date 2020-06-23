import statistics, json, urllib.request, urllib.parse

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
    ma = api.get_barset(stock, "1D", 14)
    barset = ma[stock]
    k = calc_stoch(barset, 0)

    return k

def av_stochastics(av_key, stock, date):
    URL = "https://www.alphavantage.co/query?function=STOCH&symbol={}&interval=daily&fastkperiod=14&apikey={}".format(stock, av_key)
    response = urllib.request.urlopen(URL)
    json_text = response.read().decode(encoding = 'utf-8')
    response.close()

    return json.loads(json_text)["Technical Analysis: STOCH"][date]

def calc_stoch(barset, offset):
    L14 = float('inf')
    H14 = float('-inf')
    CP = barset[-1].c

    for bar in barset:
        if bar.l < L14:
            L14 = bar.l
        if bar.h > H14:
            H14 = bar.h         

    return 100 * (CP - L14) / (H14 - L14)
import alpaca_trade_api as tradeapi
import requests, json
from pprint import pprint
from config import * 
APCA_API_KEY_ID = "PKPUSVOQPFME01UQORN8"
APCA_API_SECRET_KEY = "GzbBMLz2QE02uaElMV2rzES4VtX/P0voksxOQCYd"
BASE_URL = "https://paper-api.alpaca.markets"
ORDERS_URL = BASE_URL + "/v2/orders"
BARS_URL = BASE_URL + "/v1/bars/day"
CREDENTIALS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SEC_KEY}

def see_bars(symbol):
    query = {
        "symbol" : symbol
    }
    
    GET_BARS = BARS_URL + "?symbols=AAPL"
    r = requests.get(GET_BARS, headers=CREDENTIALS)

    return r

def create_order(symbol, qty, side, type, time_in_force):
    data = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "type": type,
        "time_in_force": time_in_force
    }

    r = requests.post(ORDERS_URL, json=data, headers=CREDENTIALS)

    return json.loads(r.content)

r = see_bars("AAPL")
print(r)
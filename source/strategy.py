import alpaca_trade_api as tradeapi
import requests, json
from pprint import pprint
from config import * 

BASE_URL = "https://paper-api.alpaca.markets"
CREDENTIALS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SEC_KEY}

api = tradeapi.REST(API_KEY, SEC_KEY, BASE_URL)


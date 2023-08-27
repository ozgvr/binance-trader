import os
from dotenv import load_dotenv
from decimal import Decimal
from binance.client import Client
from binance.helpers import round_step_size
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("SECRET_KEY")

client = Client(API_KEY, API_SECRET)

exchange_info = client.get_exchange_info()
symbol_info = {}
for symbol in exchange_info["symbols"]:
    if not symbol["status"] == "TRADING":
        continue
    if not symbol["quoteAsset"] == "USDT":
        continue
    if "LEVERAGED" in symbol["permissions"]:
        continue
    symbol_info[symbol["symbol"]] = symbol

def get_step_size(symbol):
    symbol = symbol.upper()
    if symbol == "USDT":
        return 0.01
    filters = symbol_info[symbol + "USDT"]["filters"]
    step_size = 0.1
    for filter in filters:
        if filter["filterType"] == "LOT_SIZE":
            step_size = filter["stepSize"]
    return step_size

def step_size_to_precision(step_size):
    decimals = str(step_size).split(".")[1]
    for i in range(len(decimals)):
        if decimals[i] != "0":
            return i+1
    
def update_balance(symbol, balance):
    symbol = symbol.upper()
    step_size = get_step_size(symbol)
    precision = step_size_to_precision(step_size)
    balance = "{:.{}f}".format(balance, precision)
    if int(float(balance))==0:
        balance = "0"
    with open('data.json') as f:
        data = json.load(f)
        if balance == "0":
            data.pop(symbol, None)
        elif symbol in data:
            data[symbol]["quantity"] = balance
        else:
            data[symbol] = {"quantity": balance}
    with open('data.json', 'w') as f:
        json.dump(data, f)

def get_balance(symbol):
    symbol = symbol.upper()
    with open('data.json') as f:
        data = json.load(f)
        info = data.get(symbol, None)
        if info:
            return Decimal(info.get("quantity", 0))
        else:
            return Decimal(0)

def get_all_balances():
    prices = {}
    api_prices = client.get_all_tickers()
    for symbol in api_prices:
        prices[symbol["symbol"]] = symbol["price"]
    
    with open('data.json') as f:
        data = json.load(f)
        for symbol in data:
            if symbol != "USDT":
                data[symbol]["current_price"] = prices[symbol + "USDT"]
        return data
        

def buy(symbol, size):
    symbol = symbol.upper()
    
    quantity = Decimal(get_balance("USDT") * Decimal(size))
    quantity = round_step_size(quantity, get_step_size("USDT"))
    order = client.create_order(symbol=symbol + "USDT", side=client.SIDE_BUY, type=client.ORDER_TYPE_MARKET, quoteOrderQty=quantity)

    update_balance(symbol, Decimal(get_balance(symbol) + Decimal(order["executedQty"])))
    update_balance("USDT", Decimal(get_balance("USDT") - Decimal(order["cummulativeQuoteQty"])))
    
    return order

def sell(symbol, size):
    symbol = symbol.upper()
    
    quantity = Decimal(get_balance(symbol) * Decimal(size))
    quantity = round_step_size(quantity, get_step_size(symbol))
    order = client.create_order(symbol=symbol + "USDT", side=client.SIDE_SELL, type=client.ORDER_TYPE_MARKET, quantity=quantity)

    update_balance(symbol, Decimal(get_balance(symbol) - Decimal(order["executedQty"])))
    update_balance("USDT", Decimal(get_balance("USDT") + Decimal(order["cummulativeQuoteQty"])))
    
    return order
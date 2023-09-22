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


def get_balance(symbol):
    symbol = symbol.upper()
    info = client.get_asset_balance(asset=symbol)
    if info:
        free = info.get("free", 0)
        balance = str(round_step_size(free, get_step_size(symbol)))
        return Decimal(balance)
    else:
        return Decimal(0)

def get_all_balances():
    balances = {}
    client_balance = client.get_account()
    for symbol in client_balance["balances"]:
        if float(symbol["free"]) == 0:
            continue
        balances[symbol["asset"]] = {"quantity": symbol["free"]} 
    prices = {}
    api_prices = client.get_all_tickers()
    for symbol in api_prices:
        prices[symbol["symbol"]] = symbol["price"]
    
    total = 0
    for symbol in balances:
        if not symbol == "USDT":
            balances[symbol]["current_price"] = float(prices[symbol + "USDT"])
            balances[symbol]["current_value"] = "%.2f" % (float(prices[symbol + "USDT"])*float(balances[symbol]["quantity"]))
        else:
            balances[symbol]["current_price"] = 1.00
            balances[symbol]["current_value"] = "%.2f" % float(balances[symbol]["quantity"])
        total += float(balances[symbol]["current_value"])
    return balances, total
        

def buy(symbol, size):
    symbol = symbol.upper()
    
    quantity = Decimal(get_balance("USDT") * Decimal(size))
    quantity = round_step_size(quantity, get_step_size("USDT"))
    order = client.create_order(symbol=symbol + "USDT", side=client.SIDE_BUY, type=client.ORDER_TYPE_MARKET, quoteOrderQty=quantity)
    
    return order

def sell(symbol, size):
    symbol = symbol.upper()
    
    quantity = Decimal(get_balance(symbol) * Decimal(size))
    quantity = round_step_size(quantity, get_step_size(symbol))
    order = client.create_order(symbol=symbol + "USDT", side=client.SIDE_SELL, type=client.ORDER_TYPE_MARKET, quantity=quantity)
    
    return order

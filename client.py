import os
from dotenv import load_dotenv
from decimal import Decimal
from binance.client import Client
from binance.helpers import round_step_size

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("SECRET_KEY")

client = Client(API_KEY, API_SECRET)

# Define constants
USDT_SYMBOL = "USDT"
LOT_SIZE = 0.01

exchange_info = client.get_exchange_info()
symbol_info = {}
symbol_list = {}
for symbol in exchange_info["symbols"]:
    if symbol["status"] == "TRADING" and symbol["quoteAsset"] == "USDT" and not "LEVERAGED" in symbol["permissions"]:
        symbol_info[symbol["symbol"]] = symbol
        symbol_list[symbol["symbol"]] = ""


def get_step_size(symbol):
    """
    Get the step size for a given symbol.

    Args:
        symbol (str): The symbol for which to retrieve the step size.

    Returns:
        float: The step size for the given symbol.
    """
    symbol = symbol.upper()
    if symbol == USDT_SYMBOL:
        return LOT_SIZE
    filters = symbol_info.get(symbol + "USDT", {}).get("filters", [])
    step_size = next((f["stepSize"] for f in filters if f["filterType"] == "LOT_SIZE"), LOT_SIZE)
    return Decimal(step_size)

def step_size_to_precision(step_size):
    """
    Convert step size to precision.

    Args:
        step_size (float): The step size.

    Returns:
        int: The precision level.
    """
    decimals = str(step_size).split(".")[1]
    for i in range(len(decimals)):
        if decimals[i] != "0":
            return i+1

def get_balance(symbol):
    """
    Get the balance for a given symbol.

    Args:
        symbol (str): The symbol for which to retrieve the balance.

    Returns:
        Decimal: The balance for the given symbol.
    """
    symbol = symbol.upper()
    info = client.get_asset_balance(asset=symbol)
    if info:
        free = info.get("free", 0)
        free = Decimal(free)
        balance = str(round_step_size(free, get_step_size(symbol)))
        return Decimal(balance)
    else:
        return Decimal(0)

def get_all_balances():
    """
    Get all balances and their values.

    Returns:
        dict: A dictionary containing balances and their values.
        float: The total value of all balances.
    """
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
        if not symbol == USDT_SYMBOL:
            balances[symbol]["current_price"] = float(prices[symbol + "USDT"])
            balances[symbol]["current_value"] = "%.2f" % (float(prices[symbol + "USDT"])*float(balances[symbol]["quantity"]))
        else:
            balances[symbol]["current_price"] = 1.00
            balances[symbol]["current_value"] = "%.2f" % float(balances[symbol]["quantity"])
        total += float(balances[symbol]["current_value"])
    return balances, total

def buy(symbol, size):
    """
    Execute a buy order.

    Args:
        symbol (str): The symbol for the asset to buy.
        size (Decimal): The size of the order.

    Returns:
        dict: Information about the order.
    """
    symbol = symbol.upper()
    
    quantity = Decimal(get_balance(USDT_SYMBOL) * size)
    quantity = round_step_size(quantity, get_step_size(USDT_SYMBOL))
    order = client.create_order(symbol=symbol + USDT_SYMBOL, side=client.SIDE_BUY, type=client.ORDER_TYPE_MARKET, quoteOrderQty=quantity)
    
    return order

def sell(symbol, size):
    """
    Execute a sell order.
    Args:
        symbol (str): The symbol for the asset to sell.
        size (Decimal): The size of the order.

    Returns:
        dict: Information about the order.
    """
    symbol = symbol.upper()
    
    quantity = Decimal(get_balance(symbol) * size)
    quantity = round_step_size(quantity, get_step_size(symbol))
    order = client.create_order(symbol=symbol + USDT_SYMBOL, side=client.SIDE_SELL, type=client.ORDER_TYPE_MARKET, quantity=quantity)
    
    return order

def all_symbols():
    tickers = client.get_ticker()
    for ticker in tickers:
        if not ticker["symbol"] in symbol_list:
            continue
        symbol_list[ticker["symbol"]] = {"price" : ticker["lastPrice"], "change" : ticker["priceChangePercent"]}
    return symbol_list
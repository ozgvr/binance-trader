from flask import Flask, request, jsonify, render_template
from client import buy, sell, get_all_balances, all_symbols
from decimal import Decimal

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.post('/buy')
def route_buy():
    data = request.json

    symbol = data['symbol']
    size = data['size']

    try:
        try:
            order = buy(symbol,Decimal(size))
        except Exception as e:
            return jsonify({'error': str(e)})
            
        return jsonify({'order_response': order})

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.post('/sell')
def route_sell():
    data = request.json

    symbol = data['symbol']
    size = data['size']

    try:
        try:
            order = sell(symbol,Decimal(size))
        except Exception as e:
            return jsonify({'error': str(e)})
            
        return jsonify({'order_response': order})

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.get('/balance')
def route_balance():
    try:
        balances, total = get_all_balances()
    except Exception as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'total': "%.2f" % total, 'balances': balances})

@app.get('/list')
def route_list():
    try:
        symbols = all_symbols()
    except Exception as e:
        return jsonify({'error': str(e)})
    return symbols 

if __name__ == '__main__':
    app.run("127.0.0.1",port="5555",debug=True)
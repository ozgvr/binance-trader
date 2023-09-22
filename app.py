from flask import Flask, request, jsonify, render_template
from client import buy, sell, get_all_balances

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
            order = buy(symbol,size)
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
            order = sell(symbol,size)
        except Exception as e:
            return jsonify({'error': str(e)})
            
        return jsonify({'order_response': order})

    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.get('/balance')
def route_balance():
    try:
        balances = get_all_balances()
    except Exception as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'balances': balances})

if __name__ == '__main__':
    app.run("127.0.0.1",port="5555",debug=True)
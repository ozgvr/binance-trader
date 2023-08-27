# Binance Trader
Python Flask web dashboard for Binance API with real-time charts, trade execution, and portfolio management
<img width="1200" alt="image" src="https://github.com/ozgvr/binance-trader/assets/61429082/0cc0e595-b595-4d87-97f6-c4845d576bfe">
## How to get started
#### 1. Clone the repository
```
git clone https://github.com/ozgvr/binance-trader.git
```
#### 2. Install required libraries
In project directory run a pip install on requirements file
```
python -m pip install -r requirements.txt
```
#### 3. Create a .env file with your Binance API credentials
```
API_KEY=XXX
SECRET_KEY=XXX
```
#### 4. Update data.json
data.json is the file for storing your balances for the trades you make in the app. For initial usage, set your Binance cryptocurrency balances that you want to include in the app. For example, you can set a 50 USDT balance as: 
```
{
  "USDT": {
    "quantity": "50.00"
  }
}
```
Make sure that balances you set are not exceeding what you own in your Binance wallet, or the app will throw 'Insufficient funds' error for your invalid trades.
#### 5. Run Flask server
`python app.py`
#### 6. Open web dashboard in your browser
[http://127.0.0.1:5555](http://127.0.0.1:5555 "http://127.0.0.1:5555")
Default host for the server is 127.0.0.1 with port 5555. You can edit them from the app.py file.

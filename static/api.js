function fetchCryptoDataFromBinance(symbol, interval="1d") {
    const baseUrl = 'https://api.binance.com/api/v3/klines';

    const params = new URLSearchParams({
        symbol: symbol.toUpperCase()+"USDT",
        interval: interval,
        limit: 50
    });

    fetch(`${baseUrl}?${params}`)
    .then(response => response.json())
    .then(data => {
        if (data.code && data.code === -1121) {
            showAlert('Symbol not found. Please enter a valid symbol.');
        } else {
            const prices = data.map(entry => parseFloat(entry[4]));
            const timestamps = data.map(entry => {
                const timestamp = new Date(entry[6]);
                const formattedTimestamp = timestamp.toLocaleString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit',
                    second: '2-digit',
                    hour12: false,
                    h24: true,
                });
                return formattedTimestamp;
            });

            updateChart(timestamps, prices);
            document.getElementById('cryptoBase').textContent = symbol.toUpperCase();
            document.getElementById('cryptoQuote').textContent = "USDT";
            document.getElementById('selectedTicker').textContent = symbol.toUpperCase();
            document.getElementById('cryptoPrice').textContent = `$${prices[prices.length - 1]}`;
            const change = prices[prices.length - 1] - prices[0];
            const changePercentage = (change / prices[0]) * 100;
            if (change > 0) {
                document.getElementById('cryptoChange').className = 'badge bg-success';
            } else {
                document.getElementById('cryptoChange').className = 'badge bg-danger';
            }
            document.getElementById('cryptoChange').textContent = `${changePercentage.toFixed(2)}%`;
            document.getElementById('timeframes').classList.remove('d-none');
        }
        
    })
    .catch(error => {
        console.error('Error fetching crypto data:', error);
        showAlert('An error occurred while fetching data. Please try again later.');
    });
    timeFrameButtons.forEach(button => {
            button.classList.remove('active');
    });
    document.querySelector('.btn-timeframe[value="' + interval + '"]').classList.add('active');
}


async function executeTrade(symbol, side) {
    const baseUrl = 'http://127.0.0.1:5555';

    const params = new URLSearchParams({
        symbol: symbol,
    });

    const queryString = params.toString();
    
    const endpoint = side === 'BUY' ? '/buy' : '/sell';
    if (endpoint == null){
        return;
    }

    const response = await fetch(`${baseUrl}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            symbol: symbol,
            size: document.getElementById("orderPercentage").value,
        })
    });

    const data = await response.json();
    fetchBalances();
    if (data.error){
        showAlert(data.error);
    }
}

// Function to fetch balances
async function fetchBalances() {
    const url = 'http://127.0.0.1:5555';
    const response = await fetch(`${url}/balance`);
    const data = await response.json();
    const balancesList = document.getElementById('balances');
    const totalValue = document.getElementById('total-value');
    totalValue.textContent = "$ " + data.total;
    balancesList.innerHTML = '';
    for (const [balance, info] of Object.entries(data.balances)) {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item align-items-center justify-content-between';
        const listSymbol = document.createElement('span');
        listSymbol.className = 'fs-5 fw-bold';
        listSymbol.textContent = balance;
        const listBalance = document.createElement('span');
        listBalance.className = 'float-end align-self-center';
        listBalance.textContent = info.quantity;
        listItem.appendChild(listSymbol);
        const line = document.createElement('p');
        line.className = 'd-flex justify-content-between mb-0';
        const listCurrentPrice = document.createElement('span');
        listCurrentPrice.className = 'text-muted';
        listCurrentPrice.textContent = "$ " + info.current_price;
        const listCurrentValue = document.createElement('span');
        listCurrentValue.className = 'text-muted';
        listCurrentValue.textContent = "$ " + info.current_value;
        line.appendChild(listCurrentPrice);
        line.appendChild(listCurrentValue);
        listItem.appendChild(listBalance);
        listItem.appendChild(line);
        balancesList.appendChild(listItem);
    }
}
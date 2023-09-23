var ctx = document.getElementById('cryptoChart').getContext('2d');

var chartData = {
    labels: [],
    datasets: [{
        label: '',
        data: [],
        borderColor: 'white',
        fill: true,
        cubicInterpolationMode: 'default',
        tension: 0.2,
        pointRadius: 0,
        pointHitRadius: 10,
        pointHoverRadius: 10,
    }]
};

var chartOptions = {
    
    scales: {
        x: {
            display: false // Hide x-axis labels
        },
        y: {
            display: true // Hide y-axis labels
        }
    },
    plugins: {
        legend: {
            display: false // Hide legend
        },
        tooltip: {
            position: 'nearest',
            bodyFont: {
                size: 18
            },
            displayColors: false,

        }

    }
};

var myChart = new Chart(ctx, {
    type: 'line',
    data: chartData,
    options: chartOptions
});

const UPDATE_INTERVAL = 5000;

let updateInterval; // To hold the update interval reference

function updateChartData(symbol, interval) {
    fetchCryptoDataFromBinance(symbol, interval);
}

function fetchAndUpdateData(symbol, interval) {
    fetchBalances();
    updateChartData(symbol, interval);
    updateInterval = setTimeout(() => fetchAndUpdateData(symbol, interval), UPDATE_INTERVAL);
}

document.getElementById('fetch-form').addEventListener('submit', async function (event) {
    window.location.hash = document.getElementById('symbol-input').value;
});



document.getElementById('buy-btn').addEventListener('click', () => {
    const symbol = document.getElementById('cryptoBase').innerText.toUpperCase();
    if(document.getElementById("selectedTicker").innerText == ""){
        showAlert("No ticker selected");
    }else if(document.getElementById("orderPercentage").value == 0){
        showAlert("Order size cannot be 0");
    }else{
        executeTrade(symbol, 'BUY');
    }
});

document.getElementById('sell-btn').addEventListener('click', () => {
    const symbol = document.getElementById('cryptoBase').innerText.toUpperCase();
    if(document.getElementById("selectedTicker").innerText == ""){
        showAlert("No ticker selected");
    }else if(document.getElementById("orderPercentage").value == 0){
        showAlert("Order size cannot be 0");
    }else{
        executeTrade(symbol, 'SELL');
    }
});

// Add event listener to all time frame buttons to update timeframe by their button value
const timeFrameButtons = document.querySelectorAll('.btn-timeframe');
timeFrameButtons.forEach(button => {
    button.addEventListener('click', () => {
        const symbol = document.getElementById('cryptoBase').innerText.toUpperCase();
        const interval = button.value;
        sessionStorage.setItem('interval', interval);
        if (updateInterval) {
            clearTimeout(updateInterval);
        }

        fetchAndUpdateData(symbol, interval);
    });
});

// Function to update the chart
function updateChart(labels, prices) {
    myChart.data.labels = labels;
    myChart.data.datasets[0].data = prices;
    if (prices[0] > prices[prices.length - 1]) {
        myChart.data.datasets[0].borderColor = 'rgba(220,53,69,1)';
        myChart.data.datasets[0].backgroundColor = 'rgba(220,53,69,0.3)';
    } else {
        myChart.data.datasets[0].borderColor = 'rgba(25,135,84,1)';
        myChart.data.datasets[0].backgroundColor = 'rgba(25,135,84,0.3)';
    }
    myChart.update();
}




var hashValue = window.location.hash

window.addEventListener('hashchange', function() {
    var symbol = window.location.hash.substring(1); // Get the new hash value

    document.getElementById('symbol-input').value = symbol.toUpperCase();
    // Clear the previous update interval if it exists
    if (updateInterval) {
        clearTimeout(updateInterval);
    }
    interval = sessionStorage.getItem('interval') || '1d';
    fetchAndUpdateData(symbol,interval);
});


if (hashValue) {
    var symbol = hashValue.substring(1);
    document.getElementById('symbol-input').value = symbol.toUpperCase();
    // Clear the previous update interval if it exists
    if (updateInterval) {
        clearTimeout(updateInterval);
    }
    interval = sessionStorage.getItem('interval') || '1d';
    fetchAndUpdateData(symbol,interval);
}
document.getElementById('orderPercentage').value = 0;
document.getElementById('orderPercentage').addEventListener('input', (event) => {
    document.querySelector('label[for="orderPercentage"]').textContent = "Order size : %" + event.target.value * 100;
});

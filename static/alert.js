function showAlert(message) {
    const alertDiv = document.createElement('div');
    alertDiv.style.transition = 'opacity 0.3s ease-in-out';
    alertDiv.className = 'alert alert-danger mt-3';
    alertDiv.textContent = message;

    const container = document.querySelector('#alert');
    container.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.style.opacity = '0'; // Apply fade out effect
        setTimeout(() => {
            alertDiv.remove(); // Remove the alert div after the fade out
        }, 300); // Set the fade out duration
    }, 3000);

}
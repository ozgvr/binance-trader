document.getElementById('darkModeSwitch').addEventListener('change', (event) => {
    if (event.target.checked) {
        localStorage.setItem('darkMode', 'true');
        document.body.setAttribute('data-bs-theme', 'dark');
    } else {
        localStorage.setItem('darkMode', 'false');
        document.body.setAttribute('data-bs-theme', 'light');

    }
});

if (localStorage.getItem('darkMode') === 'true') {
    document.body.setAttribute('data-bs-theme', 'dark');
    document.getElementById('darkModeSwitch').checked = true;
} else {
    document.body.setAttribute('data-bs-theme', 'light');
    document.getElementById('darkModeSwitch').checked = false;
}
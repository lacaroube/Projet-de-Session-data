window.onload = function() {
    const username = localStorage.getItem('username');
    const usernameElement = document.getElementById('username');
    usernameElement.textContent = username;
}
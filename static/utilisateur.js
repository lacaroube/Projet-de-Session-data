window.onload = function() {
    const username = sessionStorage.getItem('username');
    const usernameElement = document.getElementById('username');
    usernameElement.textContent = username;
}

fetch('../static/topBarMenu.html')
  .then(response => response.text())
  .then(data => {
    document.getElementById('topBarMenu').innerHTML = data;
    manageButtonsDisplay();
  });

function goToAvis() {
    window.location.href = "avisUtilisateur.html"
}
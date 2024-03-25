fetch('topBarMenu.html')
  .then(response => response.text())
  .then(data => {
    document.getElementById('topBarMenu').innerHTML = data;
  });
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

function get_all_ville() {
    const depart_container = document.getElementById("departure")
    const destination_container = document.getElementById("destination")

    fetch("get_cities")
        .then(response => response.json())
        .then(citiesList => {
            console.log(citiesList);
            citiesList.forEach(city=>{
            const cityElementDepart = document.createElement("option");
            cityElementDepart.innerText = city;
            const cityElementDest = document.createElement("option");
            cityElementDest.innerText = city;

            depart_container.appendChild(cityElementDepart);
            destination_container.appendChild(cityElementDest)
            })
        })
}

/*function get_voyage(){
    const voyage_container = document.getElementById("voyage-container")
    const departElement = document.querySelector('select[name="Depart"]:checked');
    const destElement = document.querySelector('select[name="Destination"]:checked');
}*/

function goToAvis() {
    window.location.href = "avisUtilisateur.html"
}
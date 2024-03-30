window.onload = function() {
    const username = sessionStorage.getItem('username');
    const usernameElement = document.getElementById('username');
    usernameElement.textContent = username;
    get_all_ville();
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

function addVoyage() {
    const departure = document.getElementById('departure').value;
    const destination = document.getElementById('destination').value;
    const dateTime = document.getElementById('date-time').value;
    const price = document.getElementById('prix').value;

    const data = postVoyage(departure, destination, dateTime, price);
}

function postVoyage(departure, destination, dateTime, price) {
    const postUrl = "add-voyage"
    return fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            departure: departure,
            destination: destination,
            date_time: dateTime,
            price: price
        })
    }).then(function (response) {
        return response.json()
    })
}

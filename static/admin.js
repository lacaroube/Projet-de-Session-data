function get_all_ville() {
    const depart_container = document.getElementById("departure")
    const destination_container = document.getElementById("destination")

    fetch("get_cities")
        .then(response => response.json())
        .then(citiesList => {
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
    event.preventDefault()
    const departure = document.getElementById('departure').value;
    const destination = document.getElementById('destination').value;
    const dateTime = document.getElementById('date-time').value;
    const price = document.getElementById('prix').value;
    let errorElement = document.getElementById("submit-error")
    errorElement.innerHTML = ""

    if(departure === destination){
        errorElement.innerHTML = "<p style='color:red'>La destination ne peut pas être la ville de départ</p>"
        return
    }

    if (new Date() > new Date(dateTime)){
        errorElement.innerHTML = "<p style='color:red'>La date du depart ne peut pas être avant la date présente</p>"
        return
    }

    if(price <= 0){
        errorElement.innerHTML = "<p style='color:red'>Le prix ne peut pas être de null ou être négatif</p>"
        return
    }

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

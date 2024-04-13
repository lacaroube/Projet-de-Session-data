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

async function addVoyage() {
    event.preventDefault()
    const departure = document.getElementById('departure').value;
    const destination = document.getElementById('destination').value;
    const dateTime = document.getElementById('date-time').value;
    const dateTimeValue = new Date(dateTime)
    const price = document.getElementById('prix').value;
    let errorElement = document.getElementById("submit-error")
    errorElement.innerHTML = ""

    if(departure === destination){
        errorElement.innerHTML = "<p style='color:red'>La destination ne peut pas être la ville de départ</p>"
        return
    }

    if (dateTime === '') {
        errorElement.innerHTML = "<p style='color:red'>La date ne peut pas être nulle</p>"
        return
    }

    if (new Date() > dateTimeValue){
        errorElement.innerHTML = "<p style='color:red'>La date du depart ne peut pas être avant la date présente</p>"
        return
    }

    if(price <= 0){
        errorElement.innerHTML = "<p style='color:red'>Le prix ne peut pas être de null ou être négatif</p>"
        return
    }

    const timeOfVoyage = dateTimeValue.getHours()
    const millisecondsBeforeVoyage = dateTimeValue.setHours(0, 0, 0, 0) - new Date().setHours(0, 0, 0, 0)
    const daysBeforeVoyage = millisecondsBeforeVoyage / (24 * 60 * 60 * 1000)

    const response = await postVoyage(departure, destination, daysBeforeVoyage, timeOfVoyage, price);
    if (response === 200) {
        errorElement.innerHTML = "<p style='color:deepskyblue'>Le voyage a bien été ajouté</p>"
    }
    else {
        errorElement.innerHTML = "<p style='color:red'>Impossible d'ajouter ce voyage</p>"
    }
}

function postVoyage(departure, destination, daysBeforeVoyage, timeOfVoyage, price) {
    let errorElement = document.getElementById("submit-error")
    errorElement.innerHTML = ""
    const postUrl = "add-voyage"
    return fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            departure: departure,
            destination: destination,
            days: daysBeforeVoyage,
            hour: timeOfVoyage,
            price: price
        })
    }).then(function (response) {
        return response.status
    })
}

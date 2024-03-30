
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

function get_voyage(){
    event.preventDefault()
    const voyage_container = document.getElementById("voyage-container")
    const departElement = document.querySelector('select[name="departure"]').value;
    const destElement = document.querySelector('select[name="destination"]').value;
    const datetimeElement = document.querySelector('input[name="date-time"]').value;
    const prixElement = document.querySelector('input[name="prix"]').value;

    const getURL = "get_voyages"

    fetch(getURL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            depart: departElement,
            destination: destElement,
            date_temps: datetimeElement,
            prix: prixElement
        })
    }).then(response => response.json())
        .then(voyage_list => {
            voyage_container.innerHTML = ""
            voyage_list.forEach(voyage => {
                const voyageElement = document.createElement("li")
                const addVoyageButton = document.createElement("button")
                addVoyageButton.innerText = "Ajouter Voyage"
                voyageElement.innerText = voyage.depart + " - " + voyage.destination + " - " + voyage.date_temps + " - " + voyage.prix

                addVoyageButton.addEventListener('click', add_voyage)

                voyageElement.appendChild(addVoyageButton)
                voyage_container.appendChild(voyageElement)
            })
            }

        )
}

function add_voyage(voyage){
    event.preventDefault()
    console.log("hello world")
}



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

                addVoyageButton.addEventListener('click', function (){
                    add_voyage(voyage.vo_ni)
                })

                voyageElement.appendChild(addVoyageButton)
                voyage_container.appendChild(voyageElement)
            })
            }

        )
}

function add_voyage(vo_ni){
    event.preventDefault()
    const voyageUtilisateurElement = document.getElementById("voyage-utilisateur")
    const getUrl = "add_voyage_utilisateur"
    fetch(getUrl, {
        method: "POST",
         headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({
            vo_ni: vo_ni,
            id_utilisateur: 1
        })
    }).then(response => response.json())
        .then(function (data){
            console.log(data)
        })



}

    /*const voyageElement = event.target.parentNode;
    const voyageDetails = voyageElement.innerText.split(" - ");

    const addedVoyageElement = document.createElement("li");
    addedVoyageElement.innerText = voyageDetails.join(" - ");

    const deleteButton = document.createElement("button");
    deleteButton.innerText = "Supprimer";
    deleteButton.addEventListener("click", function() {
        addedVoyageElement.remove();
    });

    addedVoyageElement.appendChild(deleteButton);

    const addedVoyagesContainer = document.getElementById("added-voyages-container");
    addedVoyagesContainer.appendChild(addedVoyageElement);*/



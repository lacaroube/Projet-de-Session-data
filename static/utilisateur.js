window.onload = function() {
    const username = sessionStorage.getItem('username')
    const usernameElement = document.getElementById('username')
    usernameElement.textContent = username;
    get_all_ville()
    get_voyages_utilisateur()
}

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
    let errorElement = document.getElementById("submit-error")
    const departElement = document.querySelector('select[name="departure"]').value;
    const destElement = document.querySelector('select[name="destination"]').value;
    const datetimeElement = document.querySelector('input[name="date-time"]').value;
    const prixElement = document.querySelector('input[name="prix"]').value;

    errorElement.innerHTML = ""

    if(departElement === destElement){
        errorElement.innerHTML = "<p style='color:red'>La destination ne peut pas être la ville de départ</p>"
        return
    }

    if (new Date() > new Date(datetimeElement)){
        errorElement.innerHTML = "<p style='color:red'>La date du depart ne peut pas être avant la date présente</p>"
        return
    }

    if(prixElement <= 0){
        errorElement.innerHTML = "<p style='color:red'>Le prix ne peut pas être de null ou être négatif</p>"
        return
    }

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
            if(Object.keys(voyage_list).length === 0){
                voyage_container.innerHTML = "<p style='color:black'>Aucun resultat trouver</p>"
            }
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

function add_voyage(vo_ni) {
    event.preventDefault()
    const id_utilisateur = sessionStorage.getItem('id')
    const getUrl = "add_voyage_utilisateur"
    fetch(getUrl, {
        method: "POST",
         headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({
            vo_ni: vo_ni,
            id_utilisateur: id_utilisateur
        })
    }).then(response => response.json())
        .then(function (data){
             get_voyages_utilisateur()
        })
}

function get_voyages_utilisateur() {
    const voyageUtilisateurElement = document.getElementById("voyage-utilisateur")
    const id_utilisateur = sessionStorage.getItem('id')
    fetch(`get_voyages_utilisateur/${id_utilisateur}`)
        .then(response => response.json())
        .then(voyagesList => {
            voyageUtilisateurElement.innerHTML = ""
            voyagesList.forEach(voyage => {
                const voyageElement = document.createElement("li")
                voyageElement.innerText = voyage.vo_dep + " - " + voyage.vo_dest + " - " + voyage.vo_heure_dep + " - " + voyage.vo_prix_passager + "$"
                voyageUtilisateurElement.appendChild(voyageElement)

                const suppression_voyage = document.createElement("button")
                suppression_voyage.innerText = "Supprimer"
                voyageElement.appendChild(suppression_voyage)

                suppression_voyage.addEventListener("click", function (){
                    supp_voyage(id_utilisateur, voyage.vo_ni)
                })
            })
        })
}

function supp_voyage(id_utilisateur, vo_ni) {
    fetch(`delete-voyage/${id_utilisateur}/${vo_ni}`, {
        method: "DELETE",
    })
        .then(function (response) {
            return response.json()
        }).then(function () {
            get_voyages_utilisateur()
    })
}

function goToAvis() {
    window.location.href = "avisUtilisateur.html"
}
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

/*
* Permet de chercher des voyages avec certaint parametre d'entrée
* */
function get_voyage(){
    event.preventDefault()
    const voyage_container = document.getElementById("voyage-container")
    let errorElement = document.getElementById("submit-error")
    const departElement = document.querySelector('select[name="departure"]').value;
    const destElement = document.querySelector('select[name="destination"]').value;
    const datetimeElement = document.querySelector('input[name="date-time"]').value;
    const prixElement = document.querySelector('input[name="prix"]').value;

    errorElement.innerHTML = ""

    //Permet de vérifier si la destination et la ville de départ ne sont pas les même
    if(departElement === destElement){
        errorElement.innerHTML = "<p style='color:red'>La destination ne peut pas être la ville de départ</p>"
        return
    }

    //Permet de vérifier si le parametre de date est vide
    if (datetimeElement === '') {
        errorElement.innerHTML = "<p style='color:red'>La date ne peut pas être nulle</p>"
        return
    }

    //Permet de vérifier si la date est avant la date actuelle
    if (new Date() > new Date(datetimeElement)){
        errorElement.innerHTML = "<p style='color:red'>La date du depart ne peut pas être avant la date présente</p>"
        return
    }

    //Permet de vérifier si le prix est nulle ou négatif
    if(prixElement <= 0){
        errorElement.innerHTML = "<p style='color:red'>Le prix ne peut pas être nul ou négatif</p>"
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
                voyage_container.innerHTML = "<p style='color:black'>Aucun resultat trouvé</p>"
            }
            voyage_list.forEach(voyage => {
                const voyageElement = document.createElement("li")
                const addVoyageButton = document.createElement("button")
                addVoyageButton.innerText = "Ajouter Voyage"
                voyageElement.innerText = voyage.depart + " - " + voyage.destination + " - " + voyage.date_temps + " - " + voyage.prix + "$"

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
    const error = document.getElementById("error-voyage")
    const id_utilisateur = sessionStorage.getItem('id')
    const postUrl = "add_voyage_utilisateur"
    fetch(postUrl, {
        method: "POST",
         headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({
            vo_ni: vo_ni,
            id_utilisateur: id_utilisateur
        })
    }).then(function(response) {
        if(response.status === 200){
            return response.json()
        }
        else{
            error.innerHTML = "<p style='color:red'>L'ajout de voyage a encontré une erreur</p>"
        }
    })
    .then(function(data) {
         get_voyages_utilisateur()
    })
}

function goToAvis(vo_ni) {
    sessionStorage.setItem('vo_ni', vo_ni)
    window.location.href = "avisUtilisateur.html"
}

async function get_voyages_utilisateur() {
    const voyageUtilisateurElement = document.getElementById("voyage-utilisateur")
    const id_utilisateur = sessionStorage.getItem('id')
    const error = document.getElementById("error-voyage")
    const responseAvis = await fetch(`get-all-avis/${sessionStorage.getItem('id')}`)
    const liste_avis = await responseAvis.json()

    await fetch(`get_voyages_utilisateur/${id_utilisateur}`)
        .then(function (response) {
            if(response.status === 200){
                return response.json()
            }
            else{
                error.innerHTML = "<p style='color:red'>Une erreur c'est produite</p>"
            }
        })
        .then(voyagesList => {
            voyageUtilisateurElement.innerHTML = ""
            voyagesList.forEach(voyage => {
                const voyageElement = document.createElement("li")
                voyageElement.innerText = voyage.vo_dep + " - " + voyage.vo_dest + " - " + voyage.vo_heure_dep + " - " + voyage.vo_prix_passager + "$"
                voyageUtilisateurElement.appendChild(voyageElement)

                const avis_voyage = document.createElement("button")
                avis_voyage.innerText = "Avis"
                voyageElement.appendChild(avis_voyage)


                if (liste_avis.some(function(avis) {
                    return avis.vo_ni === voyage.vo_ni
                })) {
                    const avis = liste_avis.find(function(avis_recherche) {
                        return avis_recherche.vo_ni === voyage.vo_ni
                    })
                    const avisElement = display_avis(avis)
                    avisElement.id = `avis-${avis.vo_ni}`
                    avisElement.style.display = "none"
                    avis_voyage.addEventListener("click", function (event) {
                        event.preventDefault()
                        showAvis(avis.vo_ni)
                    })
                    voyageUtilisateurElement.appendChild(avisElement)
                } else {
                    avis_voyage.addEventListener("click", function (event) {
                        event.preventDefault();
                        goToAvis(voyage.vo_ni)
                    })
                }

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
    const error = document.getElementById("error-voyage")
    fetch(`delete-voyage/${id_utilisateur}/${vo_ni}`, {
        method: "DELETE",
    })
        .then(function (response) {
            if(response.status === 200){
                return response.json()
            }
            else{
                error.innerHTML = "<p style='color:red'>La suppression a encontré une erreur</p>"
            }
        }).then(function () {
            get_voyages_utilisateur()
    })
}

function showModifyForm(vo_ni) {
    const modifyForm = document.getElementById(`modify-form-${vo_ni}`)
    if (modifyForm.style.display === "none") {
        modifyForm.style.display = "block"
    } else {
        modifyForm.style.display = "none"
    }
}

function showAvis(vo_ni) {
    const avis = document.getElementById(`avis-${vo_ni}`)
    if (avis.style.display === "none") {
        avis.style.display = "block"
    } else {
        avis.style.display = "none"
        const modifyForm = document.getElementById(`modify-form-${vo_ni}`)
        modifyForm.style.display = "none"
    }
}

function modifyAvis(vo_ni, newCommentaire, newNote){
    const error = document.getElementById("error-voyage")
    const noteValue = newNote ? newNote : 'Aucune note'
    fetch(`modify-avis/${sessionStorage.getItem('id')}/${vo_ni}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            commentaire: newCommentaire,
            note: noteValue
        })
    }).then(function (response){
        if(response.status === 200){
            return response.json()
        }
        else{
            error.innerHTML = "<p style='color:red'>La modification de l'avis a encontré une erreur</p>"
        }
    }).then(function (data){
        get_voyages_utilisateur()
    })
}

function supprimerAvis(vo_ni){
    const error = document.getElementById("error-voyage")
    fetch(`delete-avis/${sessionStorage.getItem('id')}/${vo_ni}`, {
        method: "DELETE",
    }).then(function (response) {
        if(response.status === 200){
            return response.json()
        }
        else{
            error.innerHTML = "<p style='color:red'>La suppression de l'avis a encontré une erreur</p>"
        }
    }).then(function (data){
        getAllAvis()
    })
}

function display_avis(avis) {
    const avisElement = document.createElement("li")
    avisElement.innerText = avis.commentaire + " - " + avis.note

    const modifyButton = document.createElement("button")
    modifyButton.innerText = "Modifier"
    modifyButton.onclick = function () {
        event.preventDefault();
        showModifyForm(avis.vo_ni)
    }

    const modifyForm = document.createElement("form")
    modifyForm.id = `modify-form-${avis.vo_ni}`
    modifyForm.style.display = "none"

    const newCommentaireInput = document.createElement("input")
    newCommentaireInput.type = "text"
    newCommentaireInput.name = "newCommentaire"
    newCommentaireInput.placeholder = "Entrez le nouveau commentaire"
    modifyForm.appendChild(newCommentaireInput)

    const noteLabel = document.createElement("h4")
    noteLabel.innerText = "Note"
    modifyForm.appendChild(noteLabel)

    const notes = ["Excellent", "Bien", "Modeste", "Mauvais"]
    notes.forEach(note => {
        const newNoteInput = document.createElement("input")
        newNoteInput.type = "radio"
        newNoteInput.id = note
        newNoteInput.name = "newNote"
        newNoteInput.value = note
        newNoteInput.style.display = "inline-block"
        modifyForm.appendChild(newNoteInput)

        const newNoteLabel = document.createElement("label")
        newNoteLabel.for = note
        newNoteLabel.innerText = note
        newNoteLabel.style.display = "inline-block"
        modifyForm.appendChild(newNoteLabel)
    })

    const submitButton = document.createElement("button")
    submitButton.type = "submit"
    submitButton.innerText = "Valider"
    modifyForm.appendChild(submitButton)

    modifyForm.onsubmit = function(e) {
        e.preventDefault()
        const newNoteElement = modifyForm.querySelector('input[name="newNote"]:checked');
        const newNote = newNoteElement ? newNoteElement.value : 'Aucune note';
        modifyAvis(avis.vo_ni, newCommentaireInput.value, newNote)
    }

    const avisButtonSuppression = document.createElement("button")
    avisButtonSuppression.innerText = "Supprimer"
    avisButtonSuppression.onclick = function () {supprimerAvis(avis.vo_ni)}

    avisElement.appendChild(modifyButton)
    avisElement.appendChild(modifyForm)
    avisElement.appendChild(avisButtonSuppression)

    return avisElement
}

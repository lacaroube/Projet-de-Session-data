function onAvisButtonClick(){
    const inputElement = document.getElementById("notice-input")
    const textInput = inputElement.value

    const noteElement = document.querySelector('input[name="Note"]:checked');
    const noteValue = noteElement ? noteElement.value : 'Aucune note';

    const newAvisElement = document.createElement("div")
    newAvisElement.innerText = textInput


    postAvis(textInput, noteValue)
    getAllAvis()

    inputElement.value = ""
}

function postAvis(text, note) {
    const postUrl = "add-avis"

    fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text,
            note: note
        })
    }).then(function (response) {
        return response.json()
    }).then(function (data) {
        getAllAvis();
    })
}


window.onload = getAllAvis;
function getAllAvis() {
    const avisContainer = document.getElementById("notice-containeur");
    avisContainer.innerHTML = "";

    fetch("get-avis")
        .then(response => response.json())
        .then(avisList => {
            avisList.forEach(avis => {
                const avisElement = document.createElement("li")
                avisElement.innerText = avis.commentaire + " - " + avis.note

                const modifyButton = document.createElement("button")
                modifyButton.innerText = "Modifier"
                modifyButton.onclick = function () {showModifyForm(avis.no_avis)}

                const modifyForm = document.createElement("form")
                modifyForm.id = `modify-form-${avis.no_avis}`
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
                    modifyForm.appendChild(newNoteInput)

                    const newNoteLabel = document.createElement("label")
                    newNoteLabel.for = note
                    newNoteLabel.innerText = note
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
                    modifyAvis(avis.no_avis, newCommentaireInput.value, newNote)
                }

                const avisButtonSuppression = document.createElement("button")
                avisButtonSuppression.innerText = "Supprimer"
                avisButtonSuppression.onclick = function () {supprimerAvis(avis.no_avis)}

                avisElement.appendChild(modifyButton)
                avisElement.appendChild(modifyForm)
                avisElement.appendChild(avisButtonSuppression)
                avisContainer.appendChild(avisElement)
            })
        })
}

function showModifyForm(no_avis) {
    const modifyForm = document.getElementById(`modify-form-${no_avis}`)
    modifyForm.style.display = "block"
}

function modifyAvis(no_avis, newCommentaire, newNote){
    const noteValue = newNote ? newNote : 'Aucune note'
    fetch(`modify-avis/${no_avis}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            commentaire: newCommentaire,
            note: noteValue
        })
    }).then(function (response){
        return response.json()
    }).then(function (data){
        getAllAvis()
    })
}
function supprimerAvis(no_avis){
    fetch(`delete-avis/${no_avis}`, {
        method: "DELETE",
    }).then(function (response){
        return response.json()
    }).then(function (data){
        getAllAvis()
    })
}
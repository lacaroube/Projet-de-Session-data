function onAvisButtonClick(){
    const inputElement = document.getElementById("notice-input")
    const textInput = inputElement.value

    const noteElement = document.querySelector('input[name="Note"]:checked');
    const noteValue = noteElement ? noteElement.value : 'Aucune note';

    const newAvisElement = document.createElement("div")
    newAvisElement.innerText = textInput

    postAvis(textInput, noteValue, sessionStorage.getItem('id'), sessionStorage.getItem('vo_ni'))
    inputElement.value = ""
    sessionStorage.removeItem('vo_ni')
    window.location.href = "../static/utilisateur.html"
}

function postAvis(text, note, userId, vo_ni) {
    const postUrl = "add-avis"

    fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text,
            note: note,
            user_id: userId,
            vo_ni: vo_ni
        })
    }).then(function (response) {
        return response.json()
    }).then(function (data) {
        getAllAvis();
    })
}


// window.onload = getAllAvis
function getAllAvis() {
    const avisContainer = document.getElementById("notice-containeur");
    avisContainer.innerHTML = "";

    fetch(`get-all-avis/${sessionStorage.getItem('id')}`)
        .then(response => response.json())
        .then(avisList => {
            avisList.forEach(avis => {
                const avisElement = document.createElement("li")
                avisElement.innerText = avis.commentaire + " - " + avis.note

                const modifyButton = document.createElement("button")
                modifyButton.innerText = "Modifier"
                modifyButton.onclick = function () {showModifyForm(avis.vo_ni)}

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
                    modifyAvis(avis.vo_ni, newCommentaireInput.value, newNote)
                }

                const avisButtonSuppression = document.createElement("button")
                avisButtonSuppression.innerText = "Supprimer"
                avisButtonSuppression.onclick = function () {supprimerAvis(avis.vo_ni)}

                avisElement.appendChild(modifyButton)
                avisElement.appendChild(modifyForm)
                avisElement.appendChild(avisButtonSuppression)
                avisContainer.appendChild(avisElement)
            })
        })
}

function showModifyForm(vo_ni) {
    const modifyForm = document.getElementById(`modify-form-${vo_ni}`)
    modifyForm.style.display = "block"
}

function modifyAvis(vo_ni, newCommentaire, newNote){
    const noteValue = newNote ? newNote : 'Aucune note'
    fetch(`modify-avis/${vo_ni}`, {
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

function supprimerAvis(vo_ni){
    fetch(`delete-avis/${sessionStorage.getItem('id')}/${vo_ni}`, {
        method: "DELETE",
    }).then(function (response){
        return response.json()
    }).then(function (data){
        getAllAvis()
    })
}
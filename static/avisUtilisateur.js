function onAvisButtonClick(){
    const inputElement = document.getElementById("notice-input")
    const textInput = inputElement.value

    const noteElement = document.querySelector('input[name="Note"]:checked');
    const noteValue = noteElement ? noteElement.value : 'Aucune note';

    const newAvisElement = document.createElement("div")
    newAvisElement.innerText = textInput

    const avisContainer = document.getElementById("notice-containeur")
    avisContainer.appendChild(newAvisElement)

    postAvis(textInput, noteValue)

    inputElement.value = ""
    noteElement.value = ""
}

function postAvis(text, note){
    const postUrl = "add-avis"

    fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text,
            note: note  // Ajoutez la note ici
        })
    }).then(function (response){
        return response.json()
    }).then(function (data){

    })
}
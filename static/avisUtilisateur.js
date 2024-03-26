function onAvisButtonClick(){
    const inputElement = document.getElementById("notice-input")

    const textInput = inputElement.value

    const newAvisElement = document.createElement("div")

    newAvisElement.innerText = textInput

    const avisContainer = document.getElementById("notice-containeur")
    avisContainer.appendChild(newAvisElement)
    postAvis(textInput)
    inputElement.value = ""
}

function postAvis(text){
    const postUrl = "add-avis"

    fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: text
        })
    }).then(function (response){
        return response.json()
    }).then(function (data){
        console.log(data)
    })
}

fetch('../static/topBarMenu.html')
  .then(response => response.text())
  .then(data => {
    document.getElementById('div2').innerHTML = data;
  });
async function loginAsConducteur() {
    const usernameInput = document.getElementById("username")
    const username = usernameInput.value
    const passwordInput = document.getElementById("password")
    const password = passwordInput.value
    const data = await getConducteur(username, password)
    if (data != null) {
        if (data.status === "success") {
            sessionStorage.setItem('username', data.conducteur[1]);
            sessionStorage.setItem('id', data.conducteur[0]);
            window.location.href = "/static/conducteur/conducteur.html";
        }
    }
}

function getConducteur(username, password) {
    const error = document.getElementById("error-login")
    const postUrl = "/static/conducteur/get-conducteur"
    return fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    }).then(function (response) {
       if(response.status === 200) {
           return response.json()
       } else{
            error.innerHTML = "<p style='color:red'>Nom utilisateur et/ou mot de passe invalide</p>"
        }
     })

}

function goToRegisterConducteur() {
    window.location.replace("../../static/conducteur/registerConducteur.html")
}

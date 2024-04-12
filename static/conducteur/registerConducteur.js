async function registerNewConducteur() {
    const usernameInput = document.getElementById("username")
    const username = usernameInput.value
    const passwordInput = document.getElementById("password")
    const password = passwordInput.value
    const data = await createConducteur(username, password)
    if (data.status === "success") {
        sessionStorage.setItem('username', data.conducteur[1]);
        sessionStorage.setItem('id', data.conducteur[0]);
        window.location.href = "conducteur.html"
    }
}

function createConducteur(username, password) {
    const error = document.getElementById("error-registration")
    error.innerHTML = ""
    const postUrl = "create-conducteur"
    return fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password,
        })
    }).then(function (response) {
        if(response.status === 500){
            error.innerHTML = "<p style='color:red'>Ce nom d'utilisateur est déjà utilisé</p>"
        }
        else if(response.status === 200){
            return response.json()
        }
    })
}
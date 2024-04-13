async function loginAsClient() {
    const usernameInput = document.getElementById("username")
    const username = usernameInput.value
    const passwordInput = document.getElementById("password")
    const password = passwordInput.value

    const data = await getClient(username, password)
    if (data.status === "success") {
        sessionStorage.setItem('username', data.client[1]);
        sessionStorage.setItem('id', data.client[0]);
        window.location.href = "client.html";
    }
}

function getClient(username, password) {
    const error = document.getElementById("error-login")
    const getUrl = "get-client"
    return fetch(getUrl, {
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

function goToRegisterClient() {
    window.location.replace("registerClient.html")
}

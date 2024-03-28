function loginAsClient() {
    const usernameInput = document.getElementById("username")
    const username = usernameInput.value
    const passwordInput = document.getElementById("password")
    const password = passwordInput.value

    getClient(username, password)
    window.location.replace("/")
}

function getClient(username, password) {
    const getUrl = "get-client"
    fetch(getUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    }).then(function (response) {
        return response.json()
    }).then(function (data) {
        return data["clients"]
    })
}

function goToRegisterClient() {
    window.location.replace("../static/register.html")
}

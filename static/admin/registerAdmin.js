async function registerNewAdmin() {
    const usernameInput = document.getElementById("username")
    const username = usernameInput.value
    const passwordInput = document.getElementById("password")
    const password = passwordInput.value

    if (username === "" || password === "") {
        document.getElementById("error-registration").innerHTML = "<p style='color:red'>Veuillez remplir tous les champs</p>"
        return
    }
    const data = await createAdmin(username, password)
    if(data != null){
        if (data.status === "success") {
            sessionStorage.setItem('username', data.admin[1]);
            sessionStorage.setItem('id', data.admin[0]);
            window.location.href = "admin.html";
        }
    }
}

function createAdmin(username, password) {
    const error = document.getElementById("error-registration")
    const postUrl = "create-admin"
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

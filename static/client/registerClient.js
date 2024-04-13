async function registerNewClient() {
    const usernameInput = document.getElementById("username")
    const username = usernameInput.value
    const passwordInput = document.getElementById("password")
    const password = passwordInput.value
    const lastNameInput = document.getElementById("last_name")
    const lastName = lastNameInput.value
    const firstNameInput = document.getElementById("first_name")
    const firstName = firstNameInput.value
    const phoneInput = document.getElementById("phone")
    const phone = phoneInput.value

    const data = await createClient(username, password, lastName, firstName, phone)
    if(data != null) {
        if (data.status === "success") {
            sessionStorage.setItem('username', data.client[1]);
            sessionStorage.setItem('id', data.client[0]);
            window.location.href = "client.html";
        }
    }
}

function createClient(username, password, lastName, firstName, phone) {
    const error = document.getElementById("error-registration")
    const postUrl = "create-client"
    return fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password,
            last_name: lastName,
            first_name: firstName,
            phone: phone
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
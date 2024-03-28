async function registerNewClient() {
    const idInput = document.getElementById("id")
    const id = idInput.value
    const usernameInput = document.getElementById("username")
    const username = usernameInput.value
    const passwordInput = document.getElementById("password")
    const password = passwordInput.value
    const lastNameInput = document.getElementById("last_name")
    const lastName = lastNameInput.value
    const firstNameInput = document.getElementById("first_name")
    const firstName = firstNameInput.value
    const birthDateInput = document.getElementById("birth_date")
    const birthDate = birthDateInput.value
    const phoneInput = document.getElementById("phone")
    const phone = phoneInput.value
    const addressInput = document.getElementById("address")
    const address = addressInput.value

    createClient(id, username, password, lastName, firstName, birthDate, phone, address)
    const data = await getClient(username, password)
    if (data.status === "success") {
        localStorage.setItem('username', data.client[1]);
        localStorage.setItem('id', data.client[0]);
        window.location.href = "utilisateur.html"
    }
}

function createClient(id, username, password, lastName, firstName, birthDate, phone, address) {
    const postUrl = "create-client"
    fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: id,
            username: username,
            password: password,
            last_name: lastName,
            first_name: firstName,
            birth_date: birthDate,
            phone: phone,
            address: address
        })
    }).then(function (response) {
        return response.json()
    })
}

function loginAsEmployee() {
    window.location.replace("/")
}

async function loginAsAdmin() {
    const usernameInput = document.getElementById("username")
    const username = usernameInput.value
    const passwordInput = document.getElementById("password")
    const password = passwordInput.value

    const data = await getAdmin(username, password)
    if (data.status === "success") {
        sessionStorage.setItem('username', data.client[1]);
        sessionStorage.setItem('id', data.client[0]);
        window.location.href = "admin.html";
    }
}

function getAdmin(username, password) {
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
        return response.json()
    })
}
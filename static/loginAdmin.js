async function loginAdmin() {
    const usernameInput = document.getElementById("username")
    const username = usernameInput.value
    const passwordInput = document.getElementById("password")
    const password = passwordInput.value

    const data = await getAdmin(username, password)
    if (data.status === "success") {
        sessionStorage.setItem('username', data.admin[1]);
        sessionStorage.setItem('id', data.admin[0]);
        window.location.href = "admin.html";
    }
}

function getAdmin(username, password) {
    const getUrl = "get-admin"
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

function goToRegisterAdmin() {
    window.location.replace("../static/registerAdmin.html")
}
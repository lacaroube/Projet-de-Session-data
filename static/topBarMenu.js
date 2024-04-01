function manageButtonsDisplay() {
    if (sessionStorage.getItem('username') === null) {
        document.getElementById('logOut').style.display = 'none'
        document.getElementById('loginAdmin').style.display = 'inline'
        document.getElementById('loginClient').style.display = 'inline'
    }
    else {
        document.getElementById('logOut').style.display = 'inline'
        document.getElementById('loginAdmin').style.display = 'none'
        document.getElementById('loginClient').style.display = 'none'
    }
}

function logOut() {
    sessionStorage.removeItem('username')
    sessionStorage.removeItem('username')
    window.location.replace("/")
}

function loginAdmin() {
    window.location.href = "loginAdmin.html"
}

function loginClient() {
    window.location.href = "loginClient.html"
}


function manageButtonsDisplay() {
    if (sessionStorage.getItem('username') === null) {
        document.getElementById('logOut').style.display = 'none'
        document.getElementById('loginService').style.display = 'inline'
        document.getElementById('loginEmployee').style.display = 'inline'
        document.getElementById('loginClient').style.display = 'inline'
    }
    else {
        document.getElementById('logOut').style.display = 'inline'
        document.getElementById('loginService').style.display = 'none'
        document.getElementById('loginEmployee').style.display = 'none'
        document.getElementById('loginClient').style.display = 'none'
    }
}

function logOut() {
    sessionStorage.removeItem('username')
    sessionStorage.removeItem('username')
    window.location.replace("/")
}

function loginService() {
    window.location.href = "loginService.html"
}

function loginEmployee() {
    window.location.href = "loginEmployee.html"
}

function loginClient() {
    window.location.href = "loginClient.html"
}


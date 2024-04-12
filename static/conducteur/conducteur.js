
document.addEventListener('DOMContentLoaded', async function() {
    let date = new Date();
    const day = date.getDate();
    let month = date.getMonth() + 1;
    const year = date.getFullYear();

    if(month < 10){
        month = "0" + month.toString()
    }
    const ajdDate = year + '-' +  month + '-' + day
    let lastClicked = null;
    const calendarEl = document.getElementById('calendar')
    const dateElement = document.getElementById('date')
    const heureDebutEl = document.getElementById('heure_debut')
    const heureFinEl = document.getElementById('heure_fin')
    const jourResponse = await getHoraireConducteur(sessionStorage.getItem('id'), ajdDate)
     if (jourResponse.status === "success") {
                    dateElement.innerText = ajdDate
                    heureDebutEl.innerText =jourResponse.horaire.heure_debut
                    heureFinEl.innerText = jourResponse.horaire.heure_fin
                }
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        dateClick: async function(info) {
            if (lastClicked) {
                lastClicked.style.backgroundColor = '';
            }
            info.dayEl.style.backgroundColor = '#00BFFFFF';
            lastClicked = info.dayEl;
            const dateValue = info.dateStr
            heureDebutEl.innerText = ""
            heureFinEl.innerText = ""
            let today = new Date();
            today.setHours(0, 0, 0, 0);
            let datePicked = new Date(dateValue)
            datePicked.setHours(0, 0, 0, 0);
            datePicked.setDate(datePicked.getDate() + 1);
            if (datePicked.getTime() >= today.getTime()) {
                dateElement.innerText = dateValue
                const horaireResponse = await getHoraireConducteur(sessionStorage.getItem('id'), dateValue)
                if (horaireResponse.status === "success") {
                    heureDebutEl.innerText = horaireResponse.horaire.heure_debut
                    heureFinEl.innerText = horaireResponse.horaire.heure_fin
                }
            } else {
                dateElement.innerHTML = "<p style='color:red'>Cette date est antérieure à aujourd'hui</p>"
            }
        }
    })
    calendar.render()
})



function getHoraireConducteur(id_conducteur, date) {
    const conger = document.getElementById("conger-horaire")
    conger.innerHTML = ""
    const postUrl = "../../static/conducteur/get-horaire"
    return fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id_conducteur: id_conducteur,
            date: date
        })
    }).then(function (response) {
        if(response.status === 200){
            return response.json()
        }
        if(response.status === 304){
            conger.innerHTML = "<p style='color:red'>Vous avez pris conger</p>"
        }
        else{
            conger.innerHTML = "<p style='color:red'>Autre erreur</p>"
        }
    })
}

async function submitDayOffRequest(){
    const error = document.getElementById("error-registration")
    error.innerHTML = ""
    const dateValue = document.querySelector('input[type="date"]').value
    const dateRequested = new Date(dateValue)
    const formattedDate = dateRequested.toISOString().split('T')[0];


    const dateMin = new Date()
    dateMin.setDate(dateMin.getDate() + 14)
    dateMin.setHours(0, 0, 0, 0)
    if (dateMin < dateRequested) {
        event.preventDefault()
        const response = await postDayOffRequest(sessionStorage.getItem('id'), formattedDate)
    } else {
        event.preventDefault()
        error.innerHTML = "<p style='color:red'>Il est trop tard pour demander congé à cette journée(minimum 2 semaine)</p>"
    }
}

function postDayOffRequest(id_conducteur, date) {
    const error = document.getElementById("error-registration")
    error.innerHTML = ""
    const postUrl = "../../static/conducteur/post-day-off-horaire"
    return fetch(postUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id_conducteur: id_conducteur,
            date: date
        })
    }).then(function (response) {
        if(response.status === 200){
            error.innerHTML = "<p style='color:deepskyblue'>Votre conger à été accepté</p>"
            return response.json()
        }
        if(response.status === 304){
            error.innerHTML = "<p style='color:red'>Vous avez déjà pris congé</p>"
        }
        else{
            error.innerHTML = "<p style='color:red'>Impossible de demander congé à cette journée</p>"
        }
    })
}

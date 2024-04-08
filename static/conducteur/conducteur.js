document.addEventListener('DOMContentLoaded', function() {
            let lastClicked = null;
    const calendarEl = document.getElementById('calendar')
    const dateElement = document.getElementById('date')
    const heureDebutEl = document.getElementById('heure_debut')
    const heureFinEl = document.getElementById('heure_fin')
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        dateClick: async function(info) {
            if (lastClicked) {
                lastClicked.style.backgroundColor = '';
            }
            info.dayEl.style.backgroundColor = '#00BFFFFF';
            lastClicked = info.dayEl;
            const dateValue = info.dateStr
            console.log(dateValue)
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
    const getUrl = "../../static/conducteur/get-horaire"
    return fetch(getUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({
            id_conducteur: id_conducteur,
            date: date
        })
    }).then(response => response.json())
}
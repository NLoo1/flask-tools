// Obsolete; integrated redirection via app

BASE_URL = 'http://127.0.0.1:5000'

btnStart = document.querySelector("input")
btnStart.addEventListener('click', () => {
    window.location.href = BASE_URL + "/questions/0"
})
async function ajaxToggle(pin) {
    let res = await fetch(`/pin/${pin}/toggle`)
    let data = await res.json()
    if (!data.done) {
        ajaxToggle(pin)
    }
}
async function ajaxTemperature() {
    let res = await fetch('/temperature')
    let data = await res.json()
    let query1 = document.querySelector("#temperature")
    query1.textContent = data.temperature
    let query2 = document.querySelector('#humidity')
    query2.textContent = data.humidity
}
ajaxTemperature()
setInterval(ajaxTemperature, 2000)
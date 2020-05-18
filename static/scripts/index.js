async function ajaxToggle(pin) {
    let res = await fetch(`/pin/${pin}/toggle`)
    let data = await res.json()
    let displayedState = document.querySelector(`#state${pin}`)
    displayedState.textContent = `State: ${data.state ? "ON" : "OFF"}`
    if (data.state) {
        displayedState.classList = "state-on"
    }
    else {
        displayedState.classList = 'state-off'
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
setInterval(ajaxTemperature, 3000)
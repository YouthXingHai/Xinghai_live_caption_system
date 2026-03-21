let ws = new WebSocket("ws://" + location.host + "/ws")

ws.onmessage = e => {

    let d = JSON.parse(e.data)

    document.getElementById("teleprompter").innerText = d.prompt

    let next = document.getElementById("next")
    next.innerHTML = ""

    d.next.forEach(x => {

        let div = document.createElement("div")
        div.innerText = x
        next.appendChild(div)

    })

}
let ws
let lines = []
let currentIndex = 0
let hotkeys = {}

function connect() {

    ws = new WebSocket("ws://" + location.host + "/ws")

    ws.onmessage = e => {

        let d = JSON.parse(e.data)

        lines = d.full
        currentIndex = d.index
        hotkeys = d.hotkeys

        renderPreview()

    }

    ws.onclose = () => setTimeout(connect, 1000)

}

connect()

function next() {

    ws.send(JSON.stringify({action: "next"}))

}

function prev() {

    ws.send(JSON.stringify({action: "prev"}))

}

function first() {

    ws.send(JSON.stringify({action: "first"}))

}

function last() {

    ws.send(JSON.stringify({action: "last"}))

}

document.addEventListener("keydown", e => {

    if (e.key == hotkeys.next) next()

    if (e.key == hotkeys.prev) prev()

    if (e.key == hotkeys.first) first()

    if (e.key == hotkeys.last) last()

})

function renderPreview() {

    let div = document.getElementById("preview")

    div.innerHTML = ""

    for (let i = 0; i < lines.length; i++) {

        let d = document.createElement("div")

        d.innerText = lines[i]

        // make each line clickable: send a goto action with the index
        d.style.cursor = 'pointer'
        d.onclick = () => {
            if (ws && ws.readyState === 1) {
                ws.send(JSON.stringify({ action: 'goto', index: i }))
            }
        }

        // Append first, then if it's the current line, mark and scroll it into view.
        div.appendChild(d)

        if (i == currentIndex) {
            d.className = "current"
            // Ensure the element is actually in the DOM and layout is ready before scrolling.
            requestAnimationFrame(() => d.scrollIntoView({block: "center", behavior: "smooth"}));
        }

    }

}

async function reloadScripts() {

    await fetch("/scripts/reload", {method: "POST"})

    loadScripts()

}

async function loadScripts(){
    let r = await fetch("/scripts")
    let s = await r.json()

    let select = document.getElementById("script-select")
    select.innerHTML = ""

    s.forEach(x=>{
        let opt = document.createElement("option")
        opt.value = x
        opt.text = x
        select.appendChild(opt)
    })

    // 自动选中当前剧本
    if(ws && ws.readyState===1){
        select.value = lines.script
    }
}

function switchScript(scriptName){
    if(ws && ws.readyState===1){
        ws.send(JSON.stringify({
            action:"switch",
            script: scriptName
        }))
    }
}

loadScripts()
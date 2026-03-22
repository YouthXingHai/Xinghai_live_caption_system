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

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function renderPreview() {
    let div = document.getElementById("preview")
    if (!div) return

    div.innerHTML = ""

    for (let i = 0; i < lines.length; i++) {
        let d = document.createElement("div")

        // 先转义再把中括号内的文字替换为带样式的 span（只把中括号内的文字设为红色）
        let safe = escapeHtml(lines[i] == null ? "" : lines[i])
        let highlighted = safe.replace(/\[([^\]]+)\]/g, (m, p1) => {
            return "[" + "<span style=\"color:red\">" + p1 + "</span>" + "]"
        })

        d.innerHTML = highlighted

        d.style.cursor = 'pointer'
        d.onclick = () => {
            if (ws && ws.readyState === 1) {
                ws.send(JSON.stringify({action: 'goto', index: i}))
            }
        }

        div.appendChild(d)

        if (i == currentIndex) {
            d.className = "current"
            requestAnimationFrame(() => d.scrollIntoView({block: "center", behavior: "smooth"}));
        }
    }
}


async function reloadScripts() {

    await fetch("/scripts/reload", {method: "POST"})

    loadScripts()

}

async function loadScripts() {
    let r = await fetch("/scripts")
    let s = await r.json()

    let select = document.getElementById("script-select")
    select.innerHTML = ""

    s.forEach(x => {
        let opt = document.createElement("option")
        opt.value = x
        opt.text = x
        select.appendChild(opt)
    })

    // 自动选中当前剧本
    if (ws && ws.readyState === 1) {
        select.value = lines.script
    }
}

function switchScript(scriptName) {
    if (ws && ws.readyState === 1) {
        ws.send(JSON.stringify({
            action: "switch",
            script: scriptName
        }))
    }
}

loadScripts()
let ws
let lines = []
let currentIndex = 0
let hotkeys = {}
let currentScript = null

let displayMode = false   // 屏蔽控制模式


function connect() {

    ws = new WebSocket("ws://" + location.host + "/ws")

    ws.onmessage = e => {

        let d = JSON.parse(e.data)

        // update state only if fields exist
        if (d.full) lines = d.full
        if (typeof d.index === 'number') currentIndex = d.index
        if (d.hotkeys) hotkeys = d.hotkeys
        if (d.script) currentScript = d.script

        // try to sync the script select if it exists
        const select = document.getElementById("script-select")
        if (select && currentScript) {
            // if option exists, set it
            try {
                select.value = currentScript
            } catch (e) {
                // ignore
            }
        }

        renderPreview()

    }

    ws.onclose = () => setTimeout(connect, 1000)

}

connect()


/* 控制函数 */

function next() {

    if (displayMode) return

    ws.send(JSON.stringify({action: "next"}))

}

function prev() {

    if (displayMode) return

    ws.send(JSON.stringify({action: "prev"}))

}

function first() {

    if (displayMode) return

    ws.send(JSON.stringify({action: "first"}))

}

function last() {

    if (displayMode) return

    ws.send(JSON.stringify({action: "last"}))

}


/* 键盘监听 */

document.addEventListener("keydown", e => {

    if (displayMode) {
        e.preventDefault()
        e.stopPropagation()
        return
    }

    if (e.key == hotkeys.next) next()
    if (e.key == hotkeys.prev) prev()
    if (e.key == hotkeys.first) first()
    if (e.key == hotkeys.last) last()

}, true)


/* 绑定 Display Mode 开关 */

window.addEventListener("DOMContentLoaded", () => {

    const toggle = document.getElementById("display-toggle")

    if (!toggle) return

    toggle.addEventListener("change", () => {

        displayMode = toggle.checked

        document.body.classList.toggle("display-mode", displayMode)

    })

})


/* HTML 转义 */

function escapeHtml(str) {

    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\"/g, "&quot;")
        .replace(/'/g, "&#39;")

}


/* 渲染字幕 */

function renderPreview() {

    let div = document.getElementById("preview")

    if (!div) return

    div.innerHTML = ""

    for (let i = 0; i < lines.length; i++) {

        let d = document.createElement("div")

        let safe = escapeHtml(lines[i] == null ? "" : lines[i])

        let highlighted = safe.replace(/\[([^\]]+)\]/g, (m, p1) => {
            return "[" + "<span class=\"cue-highlight\">" + p1 + "</span>" + "]"
        })

        d.innerHTML = highlighted

        d.style.cursor = "pointer"

        d.onclick = () => {

            if (displayMode) return

            if (ws && ws.readyState === 1) {

                ws.send(JSON.stringify({
                    action: "goto",
                    index: i
                }))

            }

        }

        div.appendChild(d)

        if (i == currentIndex) {

            d.className = "current"

            requestAnimationFrame(() =>
                d.scrollIntoView({
                    block: "center",
                    behavior: "smooth"
                })
            )

        }

    }

}


/* 重新加载剧本 */

async function reloadScripts() {

    if (displayMode) return

    await fetch("/scripts/reload", {method: "POST"})

    loadScripts()

}


/* 加载剧本 */

async function loadScripts() {

    let r = await fetch("/scripts")

    let s = await r.json()

    let select = document.getElementById("script-select")

    if (!select) return

    select.innerHTML = ""

    s.forEach(x => {

        let opt = document.createElement("option")

        opt.value = x
        opt.text = x

        select.appendChild(opt)

    })

    // after populating, try to set current script if server provided it
    if (currentScript) {
        try {
            select.value = currentScript
        } catch (e) {
            // ignore
        }
    }

}


/* 切换剧本 */

function switchScript(scriptName) {

    if (displayMode) return

    if (ws && ws.readyState === 1) {

        ws.send(JSON.stringify({
            action: "switch",
            script: scriptName
        }))

    }

}

loadScripts()
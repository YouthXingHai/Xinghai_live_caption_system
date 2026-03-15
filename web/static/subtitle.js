let ws = new WebSocket("ws://" + location.host + "/ws")

ws.onmessage = e => {

    let d = JSON.parse(e.data)

    document.getElementById("subtitle").innerText = d.subtitle

}
ws_sub.onopen = () => {
    console.log("字幕 WebSocket 已连接")
}

ws_sub.onmessage = e => {
    let data = JSON.parse(e.data)
    if (!data) return
    div.innerText = data.subtitle || ""
}

ws_sub.onerror = e => console.error("WebSocket 错误", e)
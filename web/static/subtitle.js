let ws_sub = new WebSocket("ws://localhost:8000/ws")
let div = document.getElementById("subtitle")

ws_sub.onopen = () => {
    console.log("字幕 WebSocket 已连接")
}

ws_sub.onmessage = e => {
    let data = JSON.parse(e.data)
    if(!data) return
    div.innerText = data.subtitle || ""
}

ws_sub.onerror = e => console.error("WebSocket 错误", e)
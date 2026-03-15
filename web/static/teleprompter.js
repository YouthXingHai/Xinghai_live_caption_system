let ws_tp = new WebSocket("ws://localhost:8000/ws")
let promptDiv = document.getElementById("prompt")
let nextDiv = document.getElementById("nextLines")
ws_tp.onmessage = e=>{
    let data = JSON.parse(e.data)
    promptDiv.innerText = data.prompt || ""
    nextDiv.innerHTML = (data.next_prompts||[]).map(l=>`<div>${l}</div>`).join("")
}
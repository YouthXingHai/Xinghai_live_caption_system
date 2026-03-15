let ws = new WebSocket("ws://localhost:8000/ws")
let scriptList = []

fetch("/scripts").then(r=>r.json()).then(list=>{
    scriptList = list
    let sel = document.getElementById("scriptSelect")
    list.forEach(name=>{
        let opt=document.createElement("option")
        opt.value=name
        opt.innerText=name
        sel.appendChild(opt)
    })
    if(list.length>0){
        sel.value=list[0]
        ws.onopen = ()=> ws.send(JSON.stringify({action:"switch", script:list[0]}))
    }
    sel.onchange = ()=> ws.send(JSON.stringify({action:"switch", script:sel.value}))
})

function next(){ ws.send(JSON.stringify({action:"next"})) }
function prev(){ ws.send(JSON.stringify({action:"prev"})) }

ws.onmessage = e=>{
    let data=JSON.parse(e.data)
    let preview=document.getElementById("preview")
    if(data.full_script){
        preview.innerHTML = data.full_script.map((line,i)=>{
            let cls = (i===data.index)?"current":""
            return `<div class="${cls}">${line}</div>`
        }).join("")
    }
}
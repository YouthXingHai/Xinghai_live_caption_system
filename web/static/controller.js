let ws = new WebSocket("ws://localhost:8000/ws")
let scriptList = []
let sel = document.getElementById("scriptSelect")
let preview = document.getElementById("preview")
let stateScript = null

function loadScripts(){
    fetch("/scripts").then(r=>r.json()).then(list=>{
        scriptList = list
        sel.innerHTML=""
        list.forEach(name=>{
            let opt=document.createElement("option")
            opt.value=name
            opt.innerText=name
            sel.appendChild(opt)
        })
        if(list.length>0 && !stateScript){
            sel.value=list[0]
            ws.send(JSON.stringify({action:"switch", script:list[0]}))
        }
    })
}

function reloadScripts(){
    fetch("/scripts/reload", {method:"POST"}).then(r=>r.json()).then(data=>{
        loadScripts()
        alert("已重新加载")
    })
}

sel.onchange = ()=>{
    stateScript = sel.value
    ws.send(JSON.stringify({action:"switch", script:sel.value}))
}

function next(){ ws.send(JSON.stringify({action:"next"})) }
function prev(){ ws.send(JSON.stringify({action:"prev"})) }

ws.onmessage = e=>{
    let data=JSON.parse(e.data)
    if(data.full_script){
        preview.innerHTML = data.full_script.map((line,i)=>{
            let cls = (i===data.index)?"current":""
            return `<div class="${cls}">${line}</div>`
        }).join("")
        // 自动滚动
        let cur = preview.querySelector(".current")
        if(cur){
            let containerHeight = preview.clientHeight
            let scrollTop = cur.offsetTop - containerHeight/2 + cur.offsetHeight/2
            preview.scrollTop = scrollTop
        }
    }
}

// 页面加载时先加载剧本
loadScripts()
import os, json, re
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# -----------------------------
# 配置
# -----------------------------
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "../scripts")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "../web/static")
WEB_DIR = os.path.join(os.path.dirname(__file__), "../web")
PROGRESS_FILE = os.path.join(os.path.dirname(__file__), "../runtime/progress.json")
TELEPROMPTER_NEXT = 5

# -----------------------------
# 脚本管理
# -----------------------------
class ScriptManager:
    def __init__(self, folder):
        self.folder = folder
        self.scripts = {}
        self.load_all_scripts()

    def load_all_scripts(self):
        for f in os.listdir(self.folder):
            if f.endswith(".txt"):
                self.scripts[f] = self.load_script(f)

    def load_script(self, name):
        path = os.path.join(self.folder, name)
        lines=[]
        with open(path,"r",encoding="utf8") as f:
            for l in f:
                t = l.strip()
                if not t: continue
                cue = bool(re.match(r"^\[.*\]$", t))
                subtitle = "" if cue else t
                lines.append({"teleprompter": t, "subtitle": subtitle, "cue": cue})
        return lines

    def list_scripts(self):
        return list(self.scripts.keys())

    def get_script(self, name):
        return self.scripts.get(name, [])

# -----------------------------
# 状态管理
# -----------------------------
class CaptionState:
    def __init__(self):
        self.current_script_name=None
        self.lines=[]
        self.index=0

    def switch_script(self, name, lines):
        self.current_script_name=name
        self.lines=lines
        self.index=0

    def next(self):
        if self.index < len(self.lines)-1:
            self.index+=1

    def prev(self):
        if self.index>0:
            self.index-=1

    def jump_top(self):
        self.index=0

    def jump_end(self):
        self.index=len(self.lines)-1

    def current_subtitle(self):
        if not self.lines: return ""
        return self.lines[self.index]["subtitle"]

    def current_prompt(self):
        if not self.lines: return ""
        return self.lines[self.index]["teleprompter"]

    def next_prompts(self,n):
        future = self.lines[self.index+1:self.index+1+n]
        return [l["teleprompter"] for l in future]

    def full_script(self):
        return [l["teleprompter"] for l in self.lines]

# -----------------------------
# WebSocket 管理
# -----------------------------
class WSManager:
    def __init__(self):
        self.clients=[]

    async def connect(self, ws):
        await ws.accept()
        self.clients.append(ws)

    def disconnect(self, ws):
        if ws in self.clients:
            self.clients.remove(ws)

    async def broadcast(self, data):
        for c in self.clients:
            try:
                await c.send_json(data)
            except:
                pass

# -----------------------------
# Progress 管理
# -----------------------------
class ProgressManager:
    def __init__(self,path):
        self.path=path
        os.makedirs(os.path.dirname(path),exist_ok=True)

    def save(self,script,index):
        with open(self.path,"w",encoding="utf8") as f:
            json.dump({"script":script,"index":index},f)

    def load(self):
        try:
            with open(self.path,"r",encoding="utf8") as f:
                return json.load(f)
        except:
            return None

# -----------------------------
# 初始化
# -----------------------------
scripts = ScriptManager(SCRIPTS_DIR)
state = CaptionState()
ws_manager = WSManager()
progress = ProgressManager(PROGRESS_FILE)

app = FastAPI()

# REST: 获取剧本列表
@app.get("/scripts")
def get_scripts():
    return JSONResponse(content=scripts.list_scripts())

# WebSocket
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws_manager.connect(ws)
    try:
        while True:
            data = await ws.receive_json()
            action = data.get("action")
            if action=="next": state.next()
            elif action=="prev": state.prev()
            elif action=="jump_top": state.jump_top()
            elif action=="jump_end": state.jump_end()
            elif action=="switch":
                name = data["script"]
                lines = scripts.get_script(name)
                state.switch_script(name, lines)
            progress.save(state.current_script_name,state.index)
            await broadcast()
    except:
        ws_manager.disconnect(ws)

async def broadcast():
    payload = {
        "subtitle": state.current_subtitle(),
        "prompt": state.current_prompt(),
        "next_prompts": state.next_prompts(TELEPROMPTER_NEXT),
        "index": state.index,
        "current_script": state.current_script_name,
        "full_script": state.full_script()
    }
    await ws_manager.broadcast(payload)

# -----------------------------
# 静态文件挂载
# -----------------------------
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/web", StaticFiles(directory=WEB_DIR, html=True), name="web")

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
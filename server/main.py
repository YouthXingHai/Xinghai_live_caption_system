from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from server.caption_state import CaptionState
from server.config_loader import Config
from server.script_manager import ScriptManager
from server.websocket_hub import WebSocketHub

config = Config("config/config.yaml")

scripts = ScriptManager("scripts")

state = CaptionState("runtime/state.yaml")

hub = WebSocketHub()

hotkeys = config.get("hotkeys")

app = FastAPI()

app.mount("/web", StaticFiles(directory="web", html=True))
app.mount("/static", StaticFiles(directory="web/static"))


def build_state():
    lines = scripts.get(state.script)

    if not lines:
        return {}

    cur = lines[state.index]

    next_lines = lines[state.index + 1:state.index + config.get("teleprompter")["next_lines"]]

    return {
        "script": state.script,
        "index": state.index,
        "subtitle": cur["subtitle"],
        "prompt": cur["teleprompter"],
        "next": [x["teleprompter"] for x in next_lines],
        "full": [x["teleprompter"] for x in lines],
        "hotkeys": hotkeys
    }


@app.get("/scripts")
def list_scripts():
    return scripts.list_scripts()


@app.post("/scripts/reload")
def reload_scripts():
    scripts.load_scripts()
    return {"status": "ok"}


@app.websocket("/ws")
async def ws(ws: WebSocket):
    await hub.connect(ws)

    await ws.send_json(build_state())

    try:

        while True:

            msg = await ws.receive_json()

            lines = scripts.get(state.script)

            if msg["action"] == "next":
                state.next(len(lines))

            if msg["action"] == "prev":
                state.prev()

            if msg["action"] == "goto":
                # Jump to a specific index (ensure integer and in bounds)
                try:
                    idx = int(msg.get("index", 0))
                except Exception:
                    idx = 0

                if idx < 0:
                    idx = 0
                if idx >= len(lines):
                    idx = max(0, len(lines) - 1)

                state.index = idx
                state.save()

            if msg["action"] == "first":
                state.first()

            if msg["action"] == "last":
                state.last(len(lines))

            if msg["action"] == "switch":
                state.script = msg["script"]
                state.index = 0
                state.save()

            data = build_state()

            await hub.broadcast(data)

    except:

        hub.disconnect(ws)
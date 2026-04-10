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

import logging
logger = logging.getLogger("uvicorn")

app = FastAPI()

app.mount("/web", StaticFiles(directory="web", html=True))
app.mount("/static", StaticFiles(directory="web/static"))


def build_state():
    # get the lines for the currently selected script (may be empty)
    lines = scripts.get(state.script) or []

    # ensure index is within bounds
    if lines:
        if state.index < 0:
            state.index = 0
        if state.index >= len(lines):
            state.index = max(0, len(lines) - 1)

        cur = lines[state.index]

        subtitle = cur.get("subtitle", "")
        prompt = cur.get("teleprompter", "")

        next_count = config.get("teleprompter").get("next_lines", 5)
        next_lines = lines[state.index + 1: state.index + 1 + next_count]

    else:
        # no lines available for the current script
        subtitle = ""
        prompt = ""
        next_lines = []

    return {
        "script": state.script,
        "index": state.index,
        "subtitle": subtitle,
        "prompt": prompt,
        "next": [x.get("teleprompter", "") for x in next_lines],
        "full": [x.get("teleprompter", "") for x in lines],
        "hotkeys": hotkeys
    }


@app.get("/scripts")
def list_scripts():
    return scripts.list_scripts()


@app.post("/scripts/reload")
def reload_scripts():
    scripts.load_scripts()
    logger.info("scripts reloaded")
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
                logger.info(f"next: {state.script} -> index {state.index}")

            if msg["action"] == "prev":
                state.prev()
                logger.info(f"prev: {state.script} -> index {state.index}")

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
                logger.info(f"goto: {state.script} -> index {state.index}")

            if msg["action"] == "first":
                state.first()
                logger.info(f"first: {state.script} -> index {state.index}")

            if msg["action"] == "last":
                state.last(len(lines))
                logger.info(f"last: {state.script} -> index {state.index}")

            if msg["action"] == "switch":
                state.script = msg["script"]
                state.index = 0
                state.save()
                logger.info(f"switch to {state.script}")
            data = build_state()

            await hub.broadcast(data)

    except:

        hub.disconnect(ws)

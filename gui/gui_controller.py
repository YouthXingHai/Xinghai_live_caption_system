import sys
import json
import websocket
import yaml

from PySide6.QtWidgets import *
from PySide6.QtGui import QShortcut,QKeySequence


class Controller(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Caption Controller")

        self.ws=websocket.WebSocket()

        self.ws.connect("ws://localhost:8000/ws")

        self.label=QLabel("Ready")

        self.setCentralWidget(self.label)

        self.load_hotkeys()

    def load_hotkeys(self):

        with open("config/config.yaml") as f:

            cfg=yaml.safe_load(f)

        hk=cfg["hotkeys"]

        QShortcut(QKeySequence(hk["next"]),self,activated=self.next)

        QShortcut(QKeySequence(hk["prev"]),self,activated=self.prev)

        QShortcut(QKeySequence(hk["jump_top"]),self,activated=self.jump_top)

        QShortcut(QKeySequence(hk["jump_end"]),self,activated=self.jump_end)

    def send(self,data):

        self.ws.send(json.dumps(data))

    def next(self):
        self.send({"action":"next"})

    def prev(self):
        self.send({"action":"prev"})

    def jump_top(self):
        self.send({"action":"jump_top"})

    def jump_end(self):
        self.send({"action":"jump_end"})


if __name__=="__main__":

    app=QApplication(sys.argv)

    win=Controller()

    win.show()

    sys.exit(app.exec())
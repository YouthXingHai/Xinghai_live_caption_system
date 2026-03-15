class WebSocketHub:

    def __init__(self):
        self.clients = set()

    async def connect(self, ws):

        await ws.accept()
        self.clients.add(ws)

    def disconnect(self, ws):

        if ws in self.clients:
            self.clients.remove(ws)

    async def broadcast(self, data):

        for c in list(self.clients):

            try:
                await c.send_json(data)
            except:
                self.clients.remove(c)

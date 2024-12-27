import asyncio
import websockets

class SnakeClient:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.on_message_callback = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri)
        asyncio.create_task(self.listen())

    async def listen(self):
        async for message in self.websocket:
            if self.on_message_callback:
                self.on_message_callback(message)

    async def send(self, message):
        if self.websocket:
            await self.websocket.send(message)

    def set_on_message_callback(self, callback):
        self.on_message_callback = callback

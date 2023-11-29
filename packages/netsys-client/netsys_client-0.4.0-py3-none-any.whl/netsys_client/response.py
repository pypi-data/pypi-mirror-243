import asyncio
import websockets

class Response:

    def send_message(self, message):

        asyncio.get_event_loop().run_until_complete(self.connector(message))

    async def connector(self, message):

        uri = "ws://localhost:12345"

        async with websockets.connect(uri) as websocket:

            await websocket.send(f'{message}')
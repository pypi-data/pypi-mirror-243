import asyncio
import websockets

class Response:

    async def connector(self, message):

        uri = "ws://localhost:12345"

        async with websockets.connect(uri) as websocket:

            await websocket.send(f'{message}')

            self._response_message = await websocket.recv()

    def send_message(self, message):

        asyncio.get_event_loop().run_until_complete(self.connector(message))

    def get_response_message(self):

        return self._response_message

    
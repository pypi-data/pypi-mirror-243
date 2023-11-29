import asyncio
import websockets

class Response:

    async def connector(self, message):

        uri = "ws://localhost:12345"

        async with websockets.connect(uri) as websocket:

            print('aqui')

            await websocket.send(f'{message}')

            while True:

                print('aqui')

                self._response_message = await websocket.recv()

                print(self._response_message)

    def send_message(self, message):

        asyncio.create_task(self.connector(message))

    def get_response_message(self):

        return self._response_message

    
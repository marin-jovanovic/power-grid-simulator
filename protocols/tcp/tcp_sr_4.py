import asyncio


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):

        parts = data.decode().split(";")
        while "" in parts:
            parts.remove("")
        print("parts received", parts)

        for message in parts:

            payload = (message + " tmp").encode("utf-8") + str(";").encode("utf-8")
            print("sending", payload)
            self.transport.write(payload)

        print("done with", parts)
        print()

        # message = data.decode()
        #
        # print('Data received: {!r}'.format(message))
        #
        # print('Send: {!r}'.format(message))
        # self.transport.write(data + str("tmp").encode("utf-8"))
        #
        # print("sent")
        # # print('Close the client socket')
        # # self.transport.close()
        # print()


async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())

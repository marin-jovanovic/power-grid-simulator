import asyncio
from py.protocols.util.message import Message


class EchoServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peer_name = transport.get_extra_info('peername')
        print('Connection from {}'.format(peer_name))
        self.transport = transport

    def data_received(self, data):
        print(f"{self.transport=}")

        parts = data.decode().split(";")
        while "" in parts:
            parts.remove("")
        print("parts received", parts)

        for message in parts:

            if message == "FIN":
                self.transport.close()

            else:
                payload = (message + " tmp").encode("utf-8") + str(";").encode("utf-8")
                # payload = (message + " tmp" + ";").byte_representation()

                print("sending", payload)
                self.transport.write(payload)

        print("done with", parts)
        print()


async def async_main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()


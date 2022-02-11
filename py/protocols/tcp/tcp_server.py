import asyncio
from py.protocols.util.message import Message, MessageCodes


class EchoServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peer_name = transport.get_extra_info('peername')
        print('Connection from {}'.format(peer_name))
        self.transport = transport

    def data_received(self, data):

        messages = data.decode().split(";")
        # remove non messages
        while "" in messages:
            messages.remove("")
        print("parts received", messages)

        for i in messages:
            m = Message(i)

            if m.payload == MessageCodes.FIN.value:
                print("fin message code detected; closing connection")
                self.transport.close()

            else:
                payload = Message({"server_add_len": len(m.payload)}, str(m.payload) + " tmp")

                print("sending", payload)
                self.transport.write(payload.byte_representation())
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


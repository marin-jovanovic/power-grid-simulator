import asyncio
import datetime
from collections import defaultdict

from protocols.util.message import Message, MessageCodes


class EchoServerProtocol(asyncio.Protocol):

    def __init__(self):
        self.active_connections = defaultdict(str)

    def connection_made(self, transport):
        peer_name = transport.get_extra_info('peername')
        print('Connection from {}'.format(peer_name))
        self.transport = transport

    def data_received(self, data):

        # todo cleanup active connections after message is handled
        # todo multiple connections
        # todo multiple messages
        # partial message
        print()

        peer_name = self.transport.get_extra_info("peername")
        print("message from", peer_name, type(peer_name))

        raw_data = data.decode()

        print(datetime.datetime.now())
        print("content", raw_data)
        self.active_connections[peer_name] += raw_data

        if not raw_data.__contains__(";"):
            print("message not completed")

        raw_data = self.active_connections[peer_name]

        while raw_data.endswith(";"):
            to_process, raw_data = raw_data.split(";", 1)

            print(f"process {to_process=}")

            m = Message(to_process)

            if m.payload == MessageCodes.FIN.value:
                print("fin message code detected; closing connection")
                self.transport.close()
                # todo cleanup activate connections
                return
            else:
                payload = Message({"server_add_len": len(m.payload)},
                                  str(m.payload) + " tmp")

                print("sending", payload)
                self.transport.write(payload.byte_representation())
            # print()

            print("todo", "empty" if not raw_data else raw_data)

        self.active_connections[peer_name] = raw_data

        print("current state of log", datetime.datetime.now())

        for id, msg in self.active_connections.items():
            print(id, msg)


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

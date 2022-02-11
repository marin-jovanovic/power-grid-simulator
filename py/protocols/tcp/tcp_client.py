import asyncio
import datetime

from protocols.util.client import Client
from protocols.util.message import Message

from protocols.util.message import Message, MessageCodes

class EchoClientProtocol(asyncio.Protocol):

    def __init__(self, on_con_lost):
        self.on_con_lost = on_con_lost
        self.rec_l = []
        self.rec_q = asyncio.Queue()

        self.active_connections = defaultdict(str)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        peer_name = self.transport.get_extra_info('peername')
        # print("reply from", peer_name)

        # parts = data.decode().split(";")
        # while "" in parts:
        #     parts.remove("")

        raw_data = data.decode()

        # print(datetime.datetime.now())
        # print("content", raw_data)
        self.active_connections[peer_name] += raw_data

        # if not raw_data.__contains__(";"):
        #     print("message not completed")

        raw_data = self.active_connections[peer_name]

        parts = []

        while raw_data.endswith(";"):
            to_process, raw_data = raw_data.split(";", 1)

            # print(f"process {to_process=}")

            m = Message(to_process)
            parts.append(m)
            # ----------------- to process

            # print("todo", "empty" if not raw_data else raw_data)

        self.active_connections[peer_name] = raw_data

        # print("current state of log", datetime.datetime.now())

        # for id, msg in self.active_connections.items():
        #     print(id, msg)

        for message in parts:
            self.rec_l.append(message)
            self.rec_q.put_nowait(message)



    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


from collections import defaultdict
class TCPClient(Client):
    # todo add option to connect to multiple servers

    def __init__(self, domain_name="127.0.0.1", port=8888):
        super(TCPClient, self).__init__(domain_name, port)

        self.loop = asyncio.get_running_loop()

        self.on_con_lost = self.loop.create_future()
        self.protocol = EchoClientProtocol(self.on_con_lost)


    async def send(self, payload):
        # print("sending", payload.byte_representation())

        self.transport.write(payload.byte_representation())

    async def receive(self):


        ret = await self.protocol.rec_q.get()
        # no processing

        r = Message.decode(ret)

        self.protocol.rec_q.task_done()

        # print("received", r)
        return ret

    async def close(self):

        await self.protocol.rec_q.join()

        try:
            await self.on_con_lost
        finally:
            self.transport.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


async def tcp_client_wrapper(domain_name="127.0.0.1", port=8888):
    client = TCPClient(domain_name, port)

    client.transport, _ = await client.loop.create_connection(
        lambda: client.protocol,
        domain_name,
        port
    )

    return client


async def async_main():
    async with await tcp_client_wrapper() as p:

        await p.send(t := Message("1 aaa"))
        print("sending", t)
        # print("Data received:", await p.receive(), datetime.datetime.now(),  "\n")
        print("Data received:", await p.receive(),  "\n")

        await p.send(t := Message({"a": 1, "b": 2}))
        print("sending", t)
        print("Data received:", await p.receive(),  "\n")

        await p.send(t := Message("2 bbb"))
        print("sending", t)
        await p.send(t := Message("3 ccc"))
        print("sending", t)
        print("Data received:", await p.receive())
        print("Data received:", await p.receive(),  "\n")

        await p.send(t := Message(9999 * "xxxxxxxxx"))
        print("sending", t)
        print("Data received:", await p.receive(),  "\n")

        await p.send(t := Message("4 ddd"))
        print("sending", t)
        await p.send(t := Message("5 eee"))
        print("sending", t)
        await p.send(t := Message("FIN"))
        print("sending", t)
        print("Data received:", await p.receive())
        print("Data received:", await p.receive(),  "\n")


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()

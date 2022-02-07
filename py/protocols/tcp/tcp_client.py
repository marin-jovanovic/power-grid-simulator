import asyncio

from py.protocols.util.client import Client
from py.protocols.util.message import Message

class EchoClientProtocol(asyncio.Protocol):

    def __init__(self,  on_con_lost):
        self.on_con_lost = on_con_lost
        self.rec_l = []
        self.rec_q = asyncio.Queue()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        parts = data.decode().split(";")
        while "" in parts:
            parts.remove("")

        for message in parts:
            self.rec_l.append(message)
            self.rec_q.put_nowait(message)

            # print("rec l", self.rec_l)
            # print("rec q", self.rec_q)

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


class TCPClient(Client):

    def __init__(self, domain_name="127.0.0.1", port=8888):
        super(TCPClient, self).__init__(domain_name, port)

        self.loop = asyncio.get_running_loop()

        self.on_con_lost = self.loop.create_future()
        self.protocol = EchoClientProtocol(self.on_con_lost)

    async def send(self, payload):
        self.transport.write(payload.byte_representation())
        print("Data sent:", payload.byte_representation())
        # self.transport.write(payload.encode())
        # print('Data sent: {!r}'.format(payload))

    async def receive(self):
        ret = await self.protocol.rec_q.get()
        # no processing

        r = Message.decode(ret)

        self.protocol.rec_q.task_done()

        print("received", r)
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

        await p.send(Message("1 aaa"))
        print("Data received:", await p.receive(), "\n")

        await p.send(Message({"a":1, "b":2}, "1 aaa"))
        print("Data received:", await p.receive(), "\n")

        await p.send(Message("2 bbb"))
        await p.send(Message("3 ccc"))
        print("Data received:", await p.receive())
        print("Data received:", await p.receive(), "\n")

        await p.send(Message("4 ddd"))
        await p.send(Message("5 eee"))
        await p.send(Message("FIN"))
        print("Data received:", await p.receive())
        print("Data received:", await p.receive(), "\n")


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()
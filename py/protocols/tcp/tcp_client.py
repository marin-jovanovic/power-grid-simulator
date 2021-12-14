import asyncio

from util.client import Client

class EchoClientProtocol(asyncio.Protocol, Client):
    def __init__(self,  on_con_lost):
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        self.transport = transport

    def send_msg(self, data):
        self.transport.write(data.encode())
        print('Data sent: {!r}'.format(data))

    def data_received(self, data):

        parts = data.decode().split(";")
        while "" in parts:
            parts.remove("")

        print("parts received", parts)

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    p = EchoClientProtocol(on_con_lost)

    transport, _ = await loop.create_connection(lambda: p, '127.0.0.1', 8888)

    p.send_msg("1 aaa;")
    p.send_msg("2 bbb;")
    p.send_msg("3 ccc;")

    p.send_msg("4 ddd;")
    p.send_msg("5 eee;")
    p.send_msg("FIN;")

    try:
        await on_con_lost
    finally:
        transport.close()

if __name__ == '__main__':

    asyncio.run(main())

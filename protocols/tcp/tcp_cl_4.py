import asyncio


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self,  on_con_lost):
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        self.transport = transport

    def send_msg(self, data):
        self.transport.write(data.encode())
        print('Data sent: {!r}'.format(data))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main():
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    p = EchoClientProtocol(on_con_lost)

    transport, protocol = await loop.create_connection(
        lambda: p,
        '127.0.0.1', 8888)

    # protocol.pause_writing()
    # protocol.resume_writing()

    p.send_msg("1 aaa;")
    p.send_msg("2 bbb;")
    p.send_msg("3 ccc;")

    # try:
    #     await on_con_lost
    # finally:
    #     transport.close()
    #
    # p.send_again("2 bbb")
    p = EchoClientProtocol(on_con_lost)

    transport, protocol = await loop.create_connection(
        lambda: p,
        '127.0.0.1', 8888)

    p.send_msg("4 ddd")
    p.send_msg("5 eee")

    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main())

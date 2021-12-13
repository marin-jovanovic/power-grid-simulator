"""
utils for address translations
"""
import asyncio
import time

from hat.aio import run_asyncio
from hat.drivers import iec104

ADDRESSES = []


class Address:

    @staticmethod
    def get_as_csv(asdu_address, io_address):
        return str(asdu_address) + ";" + str(io_address)

    def __init__(self, asdu_address, io_address):
        self.asdu_address = asdu_address
        self.io_address = io_address

    def __str__(self):
        return f"{self.asdu_address=} {self.io_address=}"

    def formatted_name(self):
        return Address.get_as_csv(self.asdu_address, self.io_address)


async def load_addresses(connection=None):
    global ADDRESSES

    if not connection:
        address = iec104.Address('127.0.0.1', 19999)

        connection = await iec104.connect(address)

    raw_data = await connection.interrogate(asdu_address=65535)

    for result in raw_data:
        asdu_address = result.asdu_address
        io_address = result.io_address

        ADDRESSES.append(Address(asdu_address, io_address))

    [print(i.formatted_name()) for i in ADDRESSES]

from protocols.util.client import Client

class IEC104Client(Client):
    #     class Client(object):
    #     __metaclass__ = ABCMeta
    #
    #     def __init__(self, domain_name="127.0.0.1", port=5000):
    #         print("Client init")
    #         self.domain_name = domain_name
    #         self.port = port
    #
    #     @abstractmethod
    #     async def send(self, payload):
    #         raise NotImplementedError
    #
    #     @abstractmethod
    #     async def receive(self):
    #         raise NotImplementedError
    #
    #     @abstractmethod
    #     async def connect(self):
    #         raise NotImplementedError
    #
    #     @abstractmethod
    #     async def close(self):
    #         raise NotImplementedError

    def __init__(self, domain_name="127.0.0.1", port=5000):
        super(IEC104Client, self).__init__(domain_name, port)

        self.known_states = {}

    # todo extract to upper
    def update_states(self, new_states):
        """"""

        diff = {}

        for i in new_states:

            if (k := (i.asdu_address, i.io_address)) not in self.known_states\
                    or self.known_states[k] != i:
                diff[k] = i
                self.known_states[k] = i


        print("diff")
        for k,v in diff.items():
            print(k,v.value.value)


    async def send(self, payload):
        """"""

    async def receive(self):
        """"""

    async def receive_single(self):
        """"""

    async def receive_all(self, asdu_address):
        """"""

        states = await self.connection.interrogate(asdu_address)

        self.update_states(states)


        return states

        # raw_data = await connection.interrogate(asdu_address=65535)

    async def diff(self):
        """"""

    async def connect(self):
        """"""

    async def close(self):
        """"""


async def iec_104_init_wrapper(domain_name="127.0.0.1", port=19999):
    client = IEC104Client(domain_name, port)

    client.address = iec104.Address(domain_name, port)
    client.connection = await iec104.connect(client.address)

    return client


async def connect():
    address = iec104.Address('127.0.0.1', 19999)

    while True:

        try:
            connection = await iec104.connect(address)
            return connection

        except ConnectionRefusedError:
            n = 3
            for i in range(n):
                print("trying to reconnect in", n - i)
                await asyncio.sleep(1)
            print("reconnecting\n")


async def async_main():

    client = await iec_104_init_wrapper("127.0.0.1", 19999)
    raw_data = await client.receive_all(asdu_address=65535)
    # print()
    # print()
    # print()
    time.sleep(3)
    raw_data = await client.receive_all(asdu_address=65535)
    time.sleep(3)
    raw_data = await client.receive_all(asdu_address=65535)
    time.sleep(3)
    raw_data = await client.receive_all(asdu_address=65535)

    return

    [print(i) for i in raw_data]
    print()
    print()
    print()
    raw_data = await client.receive_all(asdu_address=65535)
    # raw_data = await connection.interrogate(asdu_address=65535)
    [print(i) for i in raw_data]

    return


    # address = iec104.Address('127.0.0.1', 19999)
    # while True:
    #     try:
    #         connection = await iec104.connect(address)
    #         break
    #     except:
    #         continue
    #
    # try:
    #     raw_data = await connection.interrogate(asdu_address=65535)
    # except:
    #     address = iec104.Address('127.0.0.1', 19999)
    #     connection = await iec104.connect(address)
    #     raw_data = await connection.interrogate(asdu_address=65535)
    #
    # [print(i) for i in raw_data]
    #
    # return

    # connection = await connect()
    # breakpoint()

    raw_data = await connection.interrogate(asdu_address=65535)
    print(len(raw_data))
    print("r", raw_data)

    while True:

        try:
            print("fetch")
            raw_data = await connection.receive()
            print("r", raw_data)

        except ConnectionError:
            print("connection lost")

            connection = await connect()


def main():
    run_asyncio(async_main())


if __name__ == '__main__':
    main()
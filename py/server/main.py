
from hat.aio import run_asyncio


async def async_main():
    server = init_modbus_server()
    # print(modbus_server)


def main():
    run_asyncio(async_main())


if __name__ == '__main__':
    main()

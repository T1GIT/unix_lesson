import asyncio


async def handle_echo(reader, writer):
    data = await reader.read(100)
    print(data)
    writer.write(data.decode().upper().encode())
    await writer.drain()
    writer.close()


async def main():
    HOST, PORT = "localhost", 8080

    server = await asyncio.start_server(handle_echo, HOST, PORT)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio


async def tcp_echo_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    message = input("Input: ")
    writer.write(message.encode())
    await writer.drain()
    data = await reader.read(100)
    print("Answer: " + data.decode())
    writer.close()
    await writer.wait_closed()


HOST, PORT = "localhost", 8080

loop = asyncio.get_event_loop()
task = loop.create_task(tcp_echo_client(HOST, PORT))
loop.run_until_complete(task)

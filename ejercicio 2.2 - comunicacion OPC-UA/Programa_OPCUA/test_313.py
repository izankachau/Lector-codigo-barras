import asyncio
from asyncua import Client

async def test():
    client = Client(url="opc.tcp://localhost:4841/freeopcua/server/")
    try:
        await client.connect()
        print("Connected successfully in Python 3.13!")
        await client.disconnect()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())

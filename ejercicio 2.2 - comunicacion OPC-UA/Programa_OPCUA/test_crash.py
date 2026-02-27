import asyncio
import builtins

# Parche de compatibilidad para Python 3.14
_original_issubclass = builtins.issubclass
def _safe_issubclass(obj, cls):
    try:
        return _original_issubclass(obj, cls)
    except TypeError:
        return False
builtins.issubclass = _safe_issubclass

from asyncua import Client

async def test():
    client = Client(url="opc.tcp://localhost:4841/freeopcua/server/")
    try:
        await client.connect()
        print("Connected!")
        await client.disconnect()
    except Exception as e:
        print(f"Error type: {type(e)}")
        print(f"Error message: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())

import asyncio
import random
import logging
from asyncua import ua, Server

async def main():
    # Configurar el servidor
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4842/freeopcua/server/")
    server.set_server_name("Simulador Maquina de Izan")

    # Configurar el namespace
    uri = "http://izan.examen.opcua"
    idx = await server.register_namespace(uri)

    # Crear la estructura de la máquina
    root = server.nodes.objects
    machine = await root.add_folder(idx, "Maquina_Produccion")
    
    # Añadir sensores
    temp = await machine.add_variable(idx, "Temperatura", 25.0)
    presion = await machine.add_variable(idx, "Presion", 1.0)
    contador = await machine.add_variable(idx, "Contador_Piezas", 0)
    marcha = await machine.add_variable(idx, "Estado_Marcha", True)

    # Hacer que las variables sean escribibles
    await temp.set_writable()
    await presion.set_writable()
    await contador.set_writable()
    await marcha.set_writable()

    print(f"Servidor OPC-UA iniciado en {server.endpoint}")
    print("Simulando datos virtuales...")

    async with server:
        count = 0
        while True:
            await asyncio.sleep(1)
            
            # Simular fluctuaciones de sensores
            val_temp = round(25 + random.uniform(-2, 2), 2)
            val_pres = round(1 + random.uniform(-0.1, 0.1), 2)
            count += 1
            
            await temp.write_value(val_temp)
            await presion.write_value(val_pres)
            await contador.write_value(count)
            
            # Si la máquina está en marcha, el contador sube
            # (En un ejemplo real, esto vendría de un PLC)

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    asyncio.run(main())

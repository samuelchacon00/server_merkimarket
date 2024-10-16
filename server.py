import asyncio,websockets,os,time,logging

port = int(os.environ.get("PORT", 8765))
print(f"Trabajando en el puerto {port}")

logging.basicConfig(level=logging.INFO)  

# Diccionario para almacenar conexiones activas
connected_clients = {}
clientes = {
    "motorola": None,
    "laptop": None,
}

async def handle_client(websocket, path):
    client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    print(f"Cliente conectado: {client_id}")

    try:
        # Mantén la conexión abierta mientras el cliente esté conectado
        while True:
            # Esperar un mensaje del cliente
            message = await websocket.recv()

            if message.startswith("laptop"):
                if not clientes["laptop"]:
                    clientes["laptop"] = {"websocket": websocket, "client_id": client_id}
                    print(f"Laptop conectado: {client_id}")
                    await websocket.send("laptop conectado")
                else:
                    if clientes["motorola"]:
                        # Enviar mensaje al motorola
                        await clientes["motorola"]["websocket"].send(message.replace("laptop/", ""))
                    else:
                        await websocket.send("Motorola no conectado!")
                        
            elif message.startswith("motorola"):
                if not clientes["motorola"]:
                    clientes["motorola"] = {"websocket": websocket, "client_id": client_id}
                    print(f"Motorola conectado: {client_id}")
                    await websocket.send("Motorola conectado")
                else:
                    if clientes["laptop"]:
                        # Enviar mensaje al laptop
                        await clientes["laptop"]["websocket"].send(message.replace("motorola/", ""))
                    else:
                        await websocket.send("Laptop no conectado!")
            else:
                print(f"Mensaje desconocido de {client_id}: {message}")

    except websockets.ConnectionClosed:
        print(f"Cliente {client_id} desconectado")
        logging.info(f"Cliente {client_id} desconectado")
        if clientes["motorola"] and clientes["motorola"]["client_id"] == client_id:
            print(f"Motorola desconectado")
            clientes["motorola"] = None
        elif clientes["laptop"] and clientes["laptop"]["client_id"] == client_id:
            print(f"Laptop desconectado")
            clientes["laptop"] = None
    finally:
        # Eliminar el cliente de la lista conectada
        if client_id in connected_clients:
            del connected_clients[client_id]


# Iniciar el servidor WebSocket
async def main():
    async with websockets.serve(handle_client, "0.0.0.0", port):
        print(f"Servidor WebSocket escuchando en el puerto {port}")
        await asyncio.Future()

asyncio.run(main())

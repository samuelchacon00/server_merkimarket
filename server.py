import asyncio
import websockets
import os

# Usa el puerto asignado por Render o uno por defecto
port = int(os.environ.get("PORT", 8765))

print(f"trabajando en el puerto {port}")

async def handle_client(websocket):
    print("Cliente conectado")
    await websocket.send("¡Bienvenido al servidor WebSocket!")
    async for message in websocket:
        print(f"Mensaje recibido del cliente: {message}")

# Iniciar el servidor WebSocket
async def main():
    async with websockets.serve(handle_client, "0.0.0.0", port):
        print(f"Servidor WebSocket escuchando en el puerto {port}")
        await asyncio.Future()  # Mantiene el servidor corriendo

asyncio.run(main())


import asyncio
import websockets

# Lista para armazenar os jogadores conectados
connected_clients = []

async def handle_client(websocket, path):
    # Adiciona o cliente à lista de conectados
    connected_clients.append(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Envia a mensagem para todos os outros clientes conectados
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)
    except websockets.exceptions.ConnectionClosedError:
        print("Client disconnected")
    finally:
        # Remove o cliente desconectado
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handle_client, "localhost", 6789):
        print("Server is running on ws://localhost:6789")
        await asyncio.Future()  # Mantém o servidor rodando indefinidamente

# Inicializa o loop de eventos e executa o servidor
if __name__ == "__main__":
    asyncio.run(main())

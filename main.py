import websockets
import asyncio

port = 5000
print("Started server on port:", port)

async def transmit(websocket, path):
    print("Client Connected!")

    try:
        while True:
            payload = await websocket.recv()

            if payload == "END_OF_STREAM":
                break

            await websocket.send(f"Sended data")
            await asyncio.sleep(5)

    except websockets.exceptions.ConnectionClosedError:
        print("Client connection closed unexpectedly.")
    except Exception as e:
        print("An error occurred:", str(e))

# Altere o host para '0.0.0.0' para permitir conexões de todas as interfaces de rede
start_server = websockets.serve(transmit, host='0.0.0.0', port=port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
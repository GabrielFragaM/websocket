import json
import websockets
import asyncio

from database import Database

port = 5000
print("Started server on port:", port)
database = Database()

async def transmit(websocket, path):
    print("Client Connected!")

    try:
        while True:
            payload = await websocket.recv()

            if payload == "END_OF_STREAM":
                break

            payload = json.loads(payload)
            
            if(payload['connection_type'] == 'notification'):
                query = database.query_notification(target_id=payload['target_id'])
                result = database.select_by_query(query, columns=[])
                print(result)
                if result['success']:
                    await websocket.send(json.dumps(result['data']))
            elif payload['connection_type'] == 'authorization':
                query = database.query_notification(target_id=payload['target_id'])
                result = database.select_by_query(query, columns=[])
                print(result)
                if result['success']:
                    await websocket.send(json.dumps(
                        {
                        "success": True,
                        "authorization_id": 'XXX',
                        "authorization_from": 'Dr. Gabriel',
                        "request_permissions": ['Ler Atestados', 'Ler Receitas', 'Histórico de exames']
                        }
                    ))
            elif payload['connection_type'] == 'pharmacies':
                query = database.query_pharmacies(uf=payload['uf'])
                result = database.select_by_query(query, columns=[])
                print(result['success'])
                print('Encontrado: ' + str(len(result['data'])) + ' resultados')
                if result['success']:
                    await websocket.send(json.dumps(result['data']))

            await asyncio.sleep(5)

    except websockets.exceptions.ConnectionClosedError:
        print("Client connection closed unexpectedly.")
    except Exception as e:
        print("An error occurred:", str(e))

# Altere o host para '0.0.0.0' para permitir conexões de todas as interfaces de rede
start_server = websockets.serve(transmit, host='0.0.0.0', port=port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
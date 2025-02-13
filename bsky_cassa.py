import asyncio
import websockets
import json
from cassandra.cluster import Cluster

# Conectar ao Cassandra
def connect_cassandra():
    cluster = Cluster(['172.17.0.2'])  # Cassandra IP
    session = cluster.connect('bluesky')  # Keyspace name
    return session

# Function insert data on cassandra
def insert_into_cassandra(session, data):
    insert_query = session.prepare("""
    INSERT INTO posts (id, text, created_at) 
    VALUES (?, ?, ?);
    """)
    session.execute(insert_query, (data['id'], data['text'], data['created_at']))

# Websocket menssages
async def process_messages():
    uri = "wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post"
    
    async with websockets.connect(uri) as websocket:
        
        while True:
            message = await websocket.recv()
            message_data = json.loads(message)

            
            print(f"Received message: {message_data}")

            
            if 'post' in message_data:
                data = {
                    'id': message_data['post'].get('id'),
                    'text': message_data['post'].get('text'),
                    'created_at': message_data['post'].get('createdAt')
                }

                # Conect to cassandra
                session = connect_cassandra()
                insert_into_cassandra(session, data)

# Run websocket
async def main():
    await process_messages()

# Asyn loop
asyncio.run(main())

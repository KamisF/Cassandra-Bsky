import asyncio
import json
import websockets
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

# Conectar ao Cassandra
cluster = Cluster(["127.17.0.2"]) 
session = cluster.connect()
session.set_keyspace("bluesky")

# Preparar query de inserção
insert_query = session.prepare("""
    INSERT INTO posts (did, time_us, kind, rev, operation, collection, rkey, created_at, text)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""")

async def consume_websocket():
    uri = "wss://jetstream2.us-east.bsky.network/subscribe\?wantedCollections=app.bsky.feed.post"
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                # Extrair dados relevantes
                did = data.get("did")
                time_us = data.get("time_us")
                kind = data.get("kind")
                commit = data.get("commit", {})
                rev = commit.get("rev")
                operation = commit.get("operation")
                collection = commit.get("collection")
                rkey = commit.get("rkey")
                created_at = commit.get("record", {}).get("createdAt")
                text = commit.get("record", {}).get("text")

                # Inserir no Cassandra
                session.execute(insert_query, (did, time_us, kind, rev, operation, collection, rkey, created_at, text))
                print(f"Inserido: {did} - {text}")

            except Exception as e:
                print(f"Erro: {e}")

# Rodar o WebSocket listener
asyncio.run(consume_websocket())

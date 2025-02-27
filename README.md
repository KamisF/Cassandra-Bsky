# Jetstream to Cassandra
A project that collects real-time data from Bluesky's Jetstream WebSocket and stores it in an Apache Cassandra database. It listens for live feed updates, parses JSON data, and inserts structured records into Cassandra for further analysis.

## 📡 Data Ingestion from Jetstream to Cassandra
This project enables real-time data ingestion from the Jetstream WebSocket API into a scalable Cassandra database. The script establishes a WebSocket connection, listens for messages, extracts relevant information, and automatically inserts the data into Cassandra.

## 🚀 Technologies
Python 3.x
WebSockets (websockets library) for real-time data streaming
Apache Cassandra for scalable NoSQL storage
cassandra-driver for database interaction
## 📦 Installation
1. Prerequisites
Ensure you have the following installed:

Python 3.x
Docker (if running Cassandra in a container)
Apache Cassandra (either Docker or local installation)
2. Install project dependencies
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/KamisF/Cassandra-Bsky.git
cd Cassandra-Bsky
```
This will install necessary Python libraries such as websockets and cassandra-driver.

3. Run Cassandra (Docker)
If using Docker, start a Cassandra container with:

```bash
docker run --name cassandra -d -p 9042:9042 cassandra
```
Verify that Cassandra is running:

```bash
docker logs cassandra
```
Or connect using cqlsh:

```bash
docker exec -it cassandra cqlsh
```
4. Create Keyspace and Table
Before running the script, create a Cassandra keyspace and table for storing data:

```bash
CREATE KEYSPACE jetstream WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE jetstream;

CREATE TABLE feed_posts (
    id UUID PRIMARY KEY,
    author TEXT,
    content TEXT,
    timestamp TIMESTAMP
);
```
## 🏃‍♀️ Running the Project
1. Start the WebSocket Listener
Run the script to start consuming real-time data from Jetstream:

```bash
python cassandra.py`
```
This will establish a connection to the Jetstream WebSocket API at:

```bash
wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post
```
The script will:
✅ Listen for new messages.
✅ Parse JSON data.
✅ Insert structured data into Cassandra.

2. Query Data in Cassandra
To verify the stored data, run:

```bash
SELECT * FROM jetstream.feed_posts;
```
## 🛠️ Troubleshooting
🔹 Connection Error to Cassandra?

Ensure Cassandra is running (docker ps or systemctl status cassandra).
Check the correct IP when using Docker (docker inspect cassandra | grep "IPAddress").

🔹 WebSocket Issues?

Ensure the Jetstream WebSocket URL is correct and active.
Restart the script if needed.

Enjoy real-time data ingestion with Jetstream & Cassandra! 🚀
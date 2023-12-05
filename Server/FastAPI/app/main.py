from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import threading
from datetime import datetime
from kafka import KafkaConsumer
import psycopg2
import json
import time

def connect_to_kafka_with_retry():
    while True:
        try:
            consumer = KafkaConsumer('coordinates', bootstrap_servers=['kafka:9092'])
            return consumer
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

def connect_to_postgresql_db():
    while True:
        try:
            db = psycopg2.connect("dbname=gpsdb user=user password=password host=postgres")
            return db
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
    

def store_message_in_db(message: bytes):
    
    msg = message.decode()
   
    parsed_msg = json.loads(msg)
    db = connect_to_postgresql_db()
    cur = db.cursor()

    cur.execute("INSERT INTO gps_coordinates (IP, LAT, LONG, timestamp) VALUES (%s, %s, %s, %s)",
                (parsed_msg['ip'], parsed_msg['lattitude'], parsed_msg['longitude'], datetime.fromtimestamp(float(parsed_msg['timestamp']))))
    db.commit()
    cur.close()
    
    print("Stored {} in database".format(parsed_msg))

def execute_db_commands():
    consumer = connect_to_kafka_with_retry()
    db = connect_to_postgresql_db()
        
        
    print("----------------------------------------")
    print("Connected to Kafka and PostgreSQL")
    print("----------------------------------------")
    commands = [
        "CREATE TABLE gps_coordinates (IP VARCHAR(20),LAT FLOAT,LONG FLOAT,timestamp TIMESTAMP,PRIMARY KEY (IP, timestamp));"
    ]

    try:
        cur = db.cursor()
        for command in commands:
            print("Executing command: " + command)
            cur.execute(command)
        cur.close()
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        print("Waiting for messages...")
        for message in consumer:
            print(message.value)
            store_message_in_db(message.value)
        print("Closing connection to Kafka and PostgreSQL")
        db.close()



app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}




db_thread = threading.Thread(target=execute_db_commands)
db_thread.start()

# List ips of connected devices
@app.get("/ips")
async def list_ips():
    db = connect_to_postgresql_db()
    cur = db.cursor()
    cur.execute("SELECT DISTINCT IP FROM gps_coordinates")
    ips = cur.fetchall()
    cur.close()
    db.close()
    return {"ips": ips}

# List coordinates of a specific device
@app.get("/coordinates/{ip}")
async def list_coordinates(ip: str):
    db = connect_to_postgresql_db()
    cur = db.cursor()
    cur.execute("SELECT LAT, LONG, timestamp FROM gps_coordinates WHERE IP = %s", (ip,))
    coordinates = cur.fetchall()
    cur.close()
    db.close()
    return {"coordinates": coordinates}

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()
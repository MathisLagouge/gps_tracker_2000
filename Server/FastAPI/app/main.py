from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
import threading
from datetime import datetime
from kafka import KafkaConsumer
import psycopg2
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
    

def store_message_in_db(message):
    db = connect_to_postgresql_db()
    cur = db.cursor()
    cur.execute("INSERT INTO gps_coordinates (IP, LAT, LONG, timestamp) VALUES (%s, %s, %s, %s)", (message['IP'], message['LAT'], message['LONG'], message['timestamp']))
    db.commit()
    cur.close()

def execute_db_commands():
    consumer = connect_to_kafka_with_retry()
    db = connect_to_postgresql_db()
        
        
    print("----------------------------------------")
    print("Connected to Kafka and PostgreSQL")
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
        while True:
            print("Waiting for messages...")
            # Fake entry to test db connection
            store_message_in_db({"IP": "172.0.0.1", "LAT": 1, "LONG": 2, "timestamp": '2021-05-20 12:07:18-09'})
            print("Message stored in db")
            for message in consumer:
                print(message.value)
                store_message_in_db(message.value)
            time.sleep(1)
        db.close()



app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()

db_thread = threading.Thread(target=execute_db_commands)
db_thread.start()

from fastapi import FastAPI, WebSocket
from kafka import KafkaConsumer
import psycopg2
import json
import time
import datetime as dt
import threading

app = FastAPI()

log_enabled = True  # Set this to False to disable logging

# Define a custom function to serialize datetime objects
def serialize_datetime(obj):
    if isinstance(obj, dt.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def log_message(message, prefix="INFO"):
    if log_enabled:
        print(f"[{prefix}] {message}")

def retry_connection(connect_function, name):
    while True:
        try:
            connection = connect_function()
            return connection
        except Exception as e:
            log_message(f"Connection to {name} failed: {e}", "ERROR")
            log_message("Retrying in 5 seconds...", "INFO")
            time.sleep(5)

def connect_to_kafka():
    return KafkaConsumer('coordinates', bootstrap_servers=['kafka:9092'])

def connect_to_postgresql():
    return psycopg2.connect("dbname=gpsdb user=user password=password host=postgres")

def store_message_in_db(message: bytes):
    msg = message.decode()
    parsed_msg = json.loads(msg)
    
    with connect_to_postgresql() as db:
        with db.cursor() as cur:
            insert_command = "INSERT INTO gps_coordinates (IP, LAT, LONG, timestamp) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
            filled_command = cur.mogrify(insert_command, (parsed_msg['ip'], parsed_msg['lattitude'], parsed_msg['longitude'],
                                                          dt.datetime.fromtimestamp(float(parsed_msg['timestamp'])).strftime("%Y-%m-%d %H:%M:%S.%f")))
            log_message(f"Filled command: {filled_command}")
            cur.execute(filled_command)
            db.commit()

    log_message(f"Stored {parsed_msg} in the database")

def execute_db_commands():
    consumer = retry_connection(connect_to_kafka, "Kafka")
    
    with connect_to_postgresql() as db:
        log_message("----------------------------------------")
        log_message("Connected to Kafka and PostgreSQL")
        log_message("----------------------------------------")
        commands = ["CREATE TABLE IF NOT EXISTS gps_coordinates (IP VARCHAR(20), LAT FLOAT, LONG FLOAT, timestamp TIMESTAMP, PRIMARY KEY (IP, timestamp));"]
        
        try:
            with db.cursor() as cur:
                for command in commands:
                    log_message(f"Executing command: {command}")
                    cur.execute(command)
                db.commit()
        except Exception as e:
            log_message(f"Error: {e}", "ERROR")
            db.rollback()
        finally:
            log_message("Waiting for messages...")
            for message in consumer:
                store_message_in_db(message.value)
            log_message("Closing connection to Kafka and PostgreSQL")

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

db_thread = threading.Thread(target=execute_db_commands)
db_thread.start()

# List IPs of connected devices
@app.get("/ips")
async def list_ips():
    with connect_to_postgresql() as db:
        with db.cursor() as cur:
            cur.execute("SELECT DISTINCT IP FROM gps_coordinates")
            ips = cur.fetchall()
    return {"ips": ips}

# List coordinates of a specific device
@app.get("/coordinates/{ip}")
async def list_coordinates(ip: str):
    with connect_to_postgresql() as db:
        with db.cursor() as cur:
            cur.execute("SELECT LAT, LONG, timestamp FROM gps_coordinates WHERE IP = %s", (ip,))
            coordinates = cur.fetchall()
    return {"coordinates": coordinates}

@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Establish a new connection for each iteration
        with connect_to_postgresql() as db:
            # Send coordinates to the client
            with db.cursor() as cur:
                cur.execute("SELECT * FROM gps_coordinates")
                coordinates = cur.fetchall()

            # Convert to map
            coordinate_map = {}
            for coordinate in coordinates:
                coordinate_map["IP"] = coordinate[0]
                coordinate_map["LAT"] = coordinate[1]
                coordinate_map["LONG"] = coordinate[2]
                coordinate_map["timestamp"] = coordinate[3]

            json_coordinates = json.dumps(coordinate_map, default=serialize_datetime)
            log_message(f"Sent coordinates to front {json_coordinates}")
            
            await websocket.send_json(json_coordinates)

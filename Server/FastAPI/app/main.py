from fastapi import FastAPI, WebSocket
from kafka import KafkaConsumer
import psycopg2
import json
import time
import datetime as dt
import threading

app = FastAPI()

# Define a custom function to serialize datetime objects
def serialize_datetime(obj):
    if isinstance(obj, dt.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def connect_to_kafka_with_retry():
    while True:
        try:
            consumer = KafkaConsumer('coordinates', bootstrap_servers=['kafka:9092'])
            return consumer
        except Exception as e:
            print(f"Connection to Kafka failed: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)


def connect_to_postgresql_db():
    while True:
        try:
            db = psycopg2.connect("dbname=gpsdb user=user password=password host=postgres")
            return db
        except Exception as e:
            print(f"Connection to PostgreSQL failed: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)


def store_message_in_db(message: bytes):
    msg = message.decode()
    parsed_msg = json.loads(msg)
    db = connect_to_postgresql_db()
    cur = db.cursor()

    insert_command = "INSERT INTO gps_coordinates (IP, LAT, LONG, timestamp) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
    filled_command = cur.mogrify(insert_command, (parsed_msg['ip'], parsed_msg['lattitude'], parsed_msg['longitude'],
                                                  dt.datetime.fromtimestamp(float(parsed_msg['timestamp'])).strftime("%Y-%m-%d %H:%M:%S.%f")))
    print("Filled command: {}".format(filled_command))

    cur.execute(filled_command)
    db.commit()
    cur.close()

    print("Stored {} in the database".format(parsed_msg))


def execute_db_commands():
    consumer = connect_to_kafka_with_retry()
    db = connect_to_postgresql_db()

    print("----------------------------------------")
    print("Connected to Kafka and PostgreSQL")
    print("----------------------------------------")
    commands = [
        "CREATE TABLE IF NOT EXISTS gps_coordinates (IP VARCHAR(20), LAT FLOAT, LONG FLOAT, timestamp TIMESTAMP, PRIMARY KEY (IP, timestamp));"
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
            store_message_in_db(message.value)
        print("Closing connection to Kafka and PostgreSQL")
        db.close()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


db_thread = threading.Thread(target=execute_db_commands)
db_thread.start()


# List IPs of connected devices
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
    while True:
        data = await websocket.receive_text()
        # Establish a new connection for each iteration
        db = connect_to_postgresql_db()

        # Send coordinates to the client
        cur = db.cursor()
        cur.execute("SELECT * FROM gps_coordinates")
        coordinates = cur.fetchall()
        cur.close()
        db.close()

        # Convert to map
        coordinate_map = {}
        for coordinate in coordinates:
            coordinate_map["IP"] = coordinate[0]
            coordinate_map["LAT"] = coordinate[1]
            coordinate_map["LONG"] = coordinate[2]
            coordinate_map["timestamp"] = coordinate[3]

        json_coordinates = json.dumps(coordinate_map, default=serialize_datetime)

        await websocket.send_json(json_coordinates)
        print("Sent coordinates to front " + json_coordinates)

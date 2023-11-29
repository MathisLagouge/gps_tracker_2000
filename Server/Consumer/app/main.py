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
    # while True:
    #     print("Waiting for messages...")
    #     for message in consumer:
    #         print(message.value)
    #         time.sleep(1)
    #     time.sleep(1)
    db.close()

    
        
    


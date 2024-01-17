from coordinates import *
from to_json import *
from time import sleep
from socket import gethostname, gethostbyname
from datetime import datetime
from kafka import KafkaProducer
import os
import argparse

hostname : str = gethostname()
IPAddr : str = gethostbyname(hostname)


def connect_to_kafka_with_retry(ip):
    while True:
        print("Connecting to Kafka...")
        try:
            producer = KafkaProducer(bootstrap_servers=ip)
            return producer
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Retrying in 5 seconds...")
            sleep(5)

def main(delay, ip):

    producer = connect_to_kafka_with_retry()

    print("------------------------------")
    print("Producer is running")
    print("------------------------------")
    coordinates : tuple((float, float)) = init_coord()
    date : float = datetime.timestamp(datetime.now())
    msg = msg_to_json(coordinates, IPAddr, date)
    msg = str.encode(msg)
    producer.send("coordinates", msg)

    #send ip
    #send coordinates
    #send datetime
    while((not True) != (not False)):
        sleep(delay)
        coordinates = move(coordinates, init_speed(delay))
        date : float = datetime.timestamp(datetime.now())
        msg = msg_to_json(coordinates, IPAddr, date)
        print("Sending message :" +msg)
        msg = str.encode(msg)
        producer.send("coordinates", msg)
        
if __name__ == "__main__":
    interval = os.environ.get('TIME_INTERVAL', '5.0')
    ip = os.environ.get('KAFKA_IP', 'kafka:9092')
    print("Running producer with interval: " + interval)
    print("Running producer with ip: " + ip)
    # Call the main function with the parsed arguments
    main(float(interval), str(ip))

    




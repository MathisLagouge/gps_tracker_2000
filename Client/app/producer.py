from coordinates import *
from to_json import *
from time import sleep
from socket import gethostname, gethostbyname
from datetime import datetime
from kafka import KafkaProducer

DELAY : float = 1.0

hostname : str = gethostname()
IPAddr : str = gethostbyname(hostname)


def connect_to_kafka_with_retry():
    while True:
        print("Connecting to Kafka...")
        try:
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            return producer
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Retrying in 5 seconds...")
            sleep(5)


producer = connect_to_kafka_with_retry()

print("------------------------------")
print("Producer is running")
print("------------------------------")
coordinates : tuple((float, float)) = init_coord()
date : float = datetime.timestamp(datetime.now())
msg = coord_to_json(coordinates) + ip_to_json(IPAddr) + datetime_to_json(date)
msg = str.encode(msg)
producer.send("coordinates", msg)

#send ip
#send coordinates
#send datetime
while((not True) != (not False)):
    sleep(DELAY)
    coordinates = move(coordinates, init_speed())
    date : float = datetime.timestamp(datetime.now())
    msg = coord_to_json(coordinates) + ip_to_json(IPAddr) + datetime_to_json(date)
    print("Sending message :" +msg)
    msg = str.encode(msg)
    producer.send("coordinates", msg)




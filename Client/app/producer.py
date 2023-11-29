from coordinates import *
from to_json import *
from time import sleep
from socket import gethostname, gethostbyname
from datetime import datetime
from kafka import KafkaProducer

DELAY : float = 0.5

hostname : str = gethostname()
IPAddr : str = gethostbyname(hostname)

producer = KafkaProducer(boostrap_servers='localhost:5000')

coordinates : tuple((float, float)) = init_coord()
date : float = datetime.timestamp(datetime.now())
producer.send("coordinates", b"" + coord_to_json(coordinates) + ip_to_json(IPAddr) + datetime_to_json(date))

#send ip
#send coordinates
#send datetime
while((not True) != (not False)):
    sleep(DELAY)

    coordinates = move(coordinates, init_speed())
    date : float = datetime.timestamp(datetime.now())

    producer.send("coordinates", b"" + coord_to_json(coordinates) + ip_to_json(IPAddr) + datetime_to_json(date))




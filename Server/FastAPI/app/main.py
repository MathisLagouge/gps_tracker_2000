from fastapi import FastAPI
from kafka import KafkaConsumer

consumer = KafkaConsumer('gps_coordinates')

for message in consumer:
    print(message)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
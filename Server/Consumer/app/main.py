from kafka import KafkaConsumer
import time

def connect_with_retry():
    while True:
        try:
            consumer = KafkaConsumer('coordinates', bootstrap_servers=['kafka:9092'])
            return consumer
        except Exception as e:
            print(f"Connection failed: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

consumer = connect_with_retry()


while True:
    print("Waiting for messages...")
    for message in consumer:
        print(message.value)
        time.sleep(1)
    time.sleep(1)
    
        
    


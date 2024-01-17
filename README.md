## gps_tracker_2000
Projet ING3 Architecture Microservices

# Author 

    - Gindro Quentin
    - Lagouge Mathis
    - Lenas Nathan
    - Ye Melody

# Run a Client

In Client/ repository

In docker-compose.yml file instert your IP

    # INSERT YOUR IP HERE

    KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://172.17.4.174:9092
    # KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092

Terminal - Client/ repository

    $- docker build . --tag 'gps-producer'

    $- docker-compose up

# Run Server

In Server/ repository

    $- docker build FastAPI/ --tag 'fastapi-ws'

    $- docker build Front/gps-tracker-2000/ --tag 'frontend'

    $- docker-compose up

In browser

    https://localhost:8080/

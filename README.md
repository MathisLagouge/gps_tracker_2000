## gps_tracker_2000
Projet ING3 Architecture Microservices

# Authors 

    - Gindro Quentin
    - Lagouge Mathis
    - Lenas Nathan
    - Ye Melody

# Run a Client

In Client/ repository

      In docker-compose.yml file insert your server machine's IP
      # Insert server IP here, for example:
        KAFKA_IP: 172.17.4.174:9092
      # KAFKA_IP: kafka:9092

Terminal - Client/ repository
    
    $- docker build . --tag 'gps-producer'
    
    $- docker-compose up

# Run Server

In Server/ repository
    
    $- docker build FastAPI/ --tag 'fastapi-ws'

    $- docker build Front/gps-tracker-2000/ --tag 'frontend'

    In docker-compose.yml file insert the server machine's IP

    # INSERT YOUR IP HERE

    KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://172.17.4.174:9092
    # KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
    
    $- docker-compose up

In browser

    https://localhost:4200/

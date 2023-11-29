# import
import random

#init coordinates (lat,long)
#return random coordinates
def init_coord() -> tuple((float,float)):

    return (random.uniform(-90,90), random.uniform(-180,180))

#init speed
#return speed vector, [-1 degres,1 degres]
def init_speed() -> tuple((float,float)):
    
    return (random.uniform(-1,1), random.uniform(-1,1))

# move
# return new position
def move(coordinates: tuple((float,float)), speed: tuple((float,float))) -> tuple((float,float)):

    latitude : float = coordinates[0] + speed[0]
    longitude : float = coordinates[1] + speed[1]

    if(latitude > 90):
        latitude = 90 - (latitude - 90)

    elif(latitude < -90):
        latitude = -90 - (latitude - 90)

    if(longitude > 180):
        latitude -= 360

    elif(longitude < -180):
        latitude += 360

    return((latitude, longitude))

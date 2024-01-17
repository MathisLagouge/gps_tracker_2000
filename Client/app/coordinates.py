# import
import random
import math

#coordinate in France for initialization
latitude_max = 48.6
latitude_min = 43.6
longitude_max = 5.7
longitude_min = -0.2

#init coordinates (lat,long)
#return random coordinates
def init_coord() -> tuple((float,float)):

    return (random.uniform(latitude_min, latitude_max), random.uniform(longitude_min, longitude_max))

#init speed
#return speed vector, [-1 degres,1 degres]
def init_speed(time: float) -> tuple((float,float)):

    alpha = random.uniform(-math.pi,math.pi)

    latitude = time * math.cos(alpha) * random.uniform(0.5,1)
    longitude = time * math.sin(alpha) * random.uniform(0.5,1)

    return (latitude / 40, longitude / 40)

# move a point
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

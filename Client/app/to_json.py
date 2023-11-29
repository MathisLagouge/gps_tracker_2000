#convert to json as string

#import
import json
import datetime

#coordinate to json as string
def coord_to_json(coordinates: tuple((float,float))) -> str :

    dict_coord: dict = {
        "lattitude": str(coordinates[0]),
        "longitude": str(coordinates[1])
    }
    
    return json.dumps(dict_coord)


#ip to json as string
def ip_to_json(ip: str) -> str:

    dict_ip: dict = {
        "ip": ip
    }

    return json.dumps(dict_ip)

    
#timestamp to json
def datetime_to_json(timestamp: float) -> str:

    dict_timestamp: dict = {
        "timestamp": str(timestamp)
    }

    return json.dumps(dict_timestamp)


# utils.py
import random
from models import zones_limitation, cars_data, user_data
import logging
import openrouteservice
from config import Config
from errors import  ErrorMessage

logger = logging.getLogger(__name__)
client = openrouteservice.Client(key=Config.ORS_API_KEY)

def get_zones_data():    
    return {
        "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [51.35, 35.78], [51.45, 35.78], [51.45, 35.72], [51.35, 35.72], [51.35, 35.78]
                ]]
            },
            "properties": {"name": "Zone 1 - North Tehran", "color": "#FF9999"}
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [51.30, 35.72], [51.40, 35.72], [51.40, 35.66], [51.30, 35.66], [51.30, 35.72]
                ]]
            },
            "properties": {"name": "Zone 2 - Central Tehran", "color": "#9999FF"}
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [51.25, 35.66], [51.38, 35.66], [51.38, 35.60], [51.25, 35.60], [51.25, 35.66]
                ]]
            },
            "properties": {"name": "Zone 3 - South Tehran", "color": "#99E099"}
        }
    ]
    }

def get_cars_data():
    return cars_data

def select_destination(user_id):
    try:
        global  current_zone

        if user_id not in user_data:
            logger.error(ErrorMessage.USER_NOT_FOUND)

            return None, None
    
        user = user_data[user_id]
        current_zone = random.choice(zones_limitation)
        car_route_conf(user)
    
        user["routes"], user["selected_route_index"] = get_route((user["lng"], user["lat"]), (user["dest_lng"], user["dest_lat"]))

        return user["dest_lat"], user["dest_lng"]
    except Exception as e:
        logger.error(ErrorMessage.DESTINATION_SELECT_ERROR)
    
def get_route(start, end):
    try:
        if not start or not end:
            logger.error(ErrorMessage.DESTINATION_NOT_DEFINED)
        route_list=[]
        response = client.directions(
            coordinates=[start, end],
            profile="driving-car",
            format="geojson",
            alternative_routes={"target_count": 3},
            radiuses=[5000, 5000]  
        )
        route_list = [feature["geometry"]["coordinates"] for feature in response["features"]]
        selected_route_index=random.randint(0, len(route_list)-1)
        return route_list, selected_route_index  
    except Exception as e:
        logger.error(ErrorMessage.FETCH_route_ERROR)
        return []  
    
def car_route_conf(user):
    try:
        if not user:
            logger.error(ErrorMessage.USER_NOT_FOUND)
            return 
        if user["car_id"]==0:
            user["dest_lat"] = random.uniform(current_zone["min_lat"], current_zone["max_lat"])
            user["dest_lng"] = random.uniform(current_zone["min_lng"], current_zone["max_lng"])
    
        if user["car_id"]==1:
            if user["dest_lat"]:
                new_dest_lat=user["beginning_lat"]
                new_dest_lng=user["beginning_lng"]
                user["beginning_lat"]=user["dest_lat"]
                user["beginning_lng"]=user["dest_lng"]
        
                user["dest_lat"]= new_dest_lat
                user["dest_lng"]=new_dest_lng
            else:
                user["dest_lat"] = random.uniform(current_zone["min_lat"], current_zone["max_lat"])
                user["dest_lng"] = random.uniform(current_zone["min_lng"], current_zone["max_lng"])
    
        if user["car_id"]==2 :
        
            zone_index=get_selected_zone(user["beginning_lat"],user["beginning_lng"], user)

            if user["dest_lat"]:
                if zones_limitation[zone_index]["min_lat"] <= user["dest_lat"] <= zones_limitation[zone_index]["max_lat"] and zones_limitation[zone_index]["min_lng"] <= user["dest_lng"] <= zones_limitation[zone_index]["max_lng"]:

                    new_dest_lat=user["beginning_lat"]
                    new_dest_lng=user["beginning_lng"]
                    user["beginning_lat"]=user["dest_lat"]
                    user["beginning_lng"]=user["dest_lng"]
                    user["dest_lat"]= new_dest_lat
                    user["dest_lng"]=new_dest_lng  
                else:
                    user["dest_lat"] = random.uniform(zones_limitation[zone_index]["min_lat"], zones_limitation[zone_index]["max_lat"])
                    user["dest_lng"] = random.uniform(zones_limitation[zone_index]["min_lng"], zones_limitation[zone_index]["max_lng"])
            else:
                user["car_id"]=0
                user["dest_lat"] = random.uniform(current_zone["min_lat"], current_zone["max_lat"])
                user["dest_lng"] = random.uniform(current_zone["min_lng"], current_zone["max_lng"])
    except Exception as e:
        logger.error(ErrorMessage.CAR_ROUTE_ERROR)
            
def get_selected_zone(lat, lng, user):
    if not user["dest_lat"]:
            user["dest_lat"] = random.uniform(current_zone["min_lat"], current_zone["max_lat"])
            user["dest_lng"] = random.uniform(current_zone["min_lng"], current_zone["max_lng"])
    i=0
    for zone in zones_limitation:
        
        if zone["min_lat"] <= lat <= zone["max_lat"] and zone["min_lng"] <= lng <= zone["max_lng"]:
            return i
        i=i+1
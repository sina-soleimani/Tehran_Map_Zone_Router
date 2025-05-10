# routes.py
from flask_socketio import  emit
from flask import request
from utils import select_destination,  get_zones_data, get_cars_data
from models import user_data, cars_data, zones_limitation
import logging
import random
from errors import ErrorMessage
from threading import Lock
lock=Lock()

logger = logging.getLogger(__name__)

socketio = None

def init_routes(app_socketio):
    try:
        global socketio
        socketio = app_socketio
        if not socketio:
            logger.error(ErrorMessage.SOCKET_NOT_EXIST)
            return
        socketio.on_event('connect', handle_connect)
        socketio.on_event('disconnect', handle_disconnect)
        socketio.on_event('get_zones', get_zones)
        socketio.on_event('get_cars', get_cars)
        socketio.on_event('change_car', change_car)
        socketio.on_event('get_locations', get_locations)
    except Exception as e:
        logger.error(ErrorMessage.SOCKET_CONNECTION_ERROR)

def handle_connect():
    try:
        user_id = request.sid
        if user_id not in user_data:
            current_zone = random.choice(zones_limitation)
            lat = random.uniform(current_zone["min_lat"], current_zone["max_lat"])
            lng = random.uniform(current_zone["min_lng"], current_zone["max_lng"])

            user_data[user_id] = {
                "lat": lat,
                "lng": lng,
                "routes": [],
                "selected_route_index": None,
                "dest_lat": None,
                "dest_lng": None,
                "beginning_lat": lat,
                "beginning_lng": lng,
                "car_id": 0
            }
        logger.info(f"User {user_id} connected")
    except Exception as e:
        logger.error(ErrorMessage.USER_CONNECTION_ERROR)

def handle_disconnect():
    
    try:
        user_id = request.sid
        if user_id in user_data:
            del user_data[user_id]
        logger.info(f"User {user_id} disconnected")
    except Exception as e:
        logger.error(ErrorMessage.USER_DISCONNECTION_ERROR)

def get_zones():
    
    try:
        zones_data = get_zones_data() 
        emit('zones_response', zones_data)
    except Exception as e:
        logger.error()
        emit('error', {'message': ErrorMessage.ZONES_NOT_EXIST})

def get_cars():
    try:
        cars_response = get_cars_data()  # A function you would implement in utils.py
        emit('cars_response', {"cars": cars_response}, broadcast=True)
    except Exception as e:
        logger.error(ErrorMessage.CARS_NOT_EXIST)
        emit('error', {'message': ErrorMessage.CARS_NOT_EXIST})

def change_car(index):
    try:
        if not index:
            logger.error(ErrorMessage.CAR_INDEX_NOT_DEFINED)
            return
        user_id = request.sid
        if not user_id:
            logger.error(ErrorMessage.USER_REQUEST_NOT_DEFINED)
            return
    
        user = user_data.get(user_id, None)
        if user:
            user["car_id"] = int(index)
            select_destination(user_id)
            emit('car_changed', {"message": "Car changed successfully"}, room=user_id)
        else:
            emit('error', {"message": ErrorMessage.USER_NOT_FOUND}, room=user_id)
            
    except Exception as e:
        logger.error(ErrorMessage.CAR_CHANGE_ERROR)
        emit('error', {'message': ErrorMessage.CAR_CHANGE_ERROR})

        

def get_locations():
    try:
        user_id = request.sid
        if not user_id:
            logger.error(ErrorMessage.USER_REQUEST_NOT_DEFINED)
            return
        if user_id not in user_data:
            return
        user = user_data[user_id]
        with lock:
            if not user["dest_lat"] or len(user["routes"])==0 or len(user["routes"][user["selected_route_index"]]) == 0:
                select_destination(user_id)
    
            if len(user["routes"]) > 0 and len(user["routes"][user["selected_route_index"]]) > 0:
                user["lng"], user["lat"] = user["routes"][user["selected_route_index"]].pop(0)

        locations_data = [{"lat":  user["lat"], "lng": user["lng"], "name": f"User {user_id}"}]
        route_data = [[{"lat": coord[1], "lng": coord[0]} for coord in route] for route in user["routes"]]
        user_data[user_id]=user

        emit('locations_response', {"locations": locations_data, "routes": route_data, "selected_car_id":user["car_id"],
                                "selected_route_index":user["selected_route_index"]}, room=user_id, )
    except Exception as e:
        logger.error(ErrorMessage.LOCATION_NOT_EXIST)

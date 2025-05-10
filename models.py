import random
user_data = {}  # Dictionary to store per-user data

zones_limitation = [
    {"min_lat": 35.72, "max_lat": 35.78, "min_lng": 51.35, "max_lng": 51.45},  # Zone 1
    {"min_lat": 35.66, "max_lat": 35.72, "min_lng": 51.30, "max_lng": 51.40},  # Zone 2
    {"min_lat": 35.60, "max_lat": 35.66, "min_lng": 51.25, "max_lng": 51.38},  # Zone 3
]

# Define zone polygons for visualization
zones_data = {
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


cars_data = []

def initialize_cars():
    global cars_data
    cars_data = []
    for i in range(3):
        zone = random.choice(zones_limitation)
        lat = random.uniform(zone["min_lat"], zone["max_lat"])
        lng = random.uniform(zone["min_lng"], zone["max_lng"])
        cars_data.append({
            "id": i,
            "lat": lat,
            "lng": lng,
            "name":f"Car {i+1}",
            "routes": [],
            "dest_lat": None,
            "dest_lng": None
        })
        
initialize_cars()


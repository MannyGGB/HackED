import googlemaps
import os
from dotenv import load_dotenv

def get_coords(address, api_key):
    gmaps = googlemaps.Client(key=api_key)
    
    # Geocoding an address
    geocode_result = gmaps.geocode(address)
    
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        return None

# Usage
load_dotenv()  # This loads the variables from .env into the system
api_key = os.getenv("MY_API_KEY")

address = "1600 Amphitheatre Parkway, Mountain View, CA"
coords = get_coords(address, api_key)

if coords:
    print(f"Address: {address}")
    print(f"Coordinates: Latitude {coords[0]}, Longitude {coords[1]}")
else:
    print("Address not found.")
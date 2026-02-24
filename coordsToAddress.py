import googlemaps
import os
from dotenv import load_dotenv

def get_address(lat, lng, api_key):
    gmaps = googlemaps.Client(key=api_key)
    
    # Reverse Geocoding
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    
    if reverse_geocode_result:
        # Returns the first formatted address match
        return reverse_geocode_result[0]['formatted_address']
    else:
        return "No address found."

load_dotenv()  # This loads the variables from .env into the system
api_key = os.getenv("MY_API_KEY")

# Example coords from your file
lat, lng = 40.714224, -73.961452

address = get_address(lat, lng, api_key)
print(f"Coordinates: {lat}, {lng}")
print(f"Address: {address}")
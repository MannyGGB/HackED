import googlemaps

def get_address(lat, lng, api_key):
    gmaps = googlemaps.Client(key=api_key)
    
    # Reverse Geocoding
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    
    if reverse_geocode_result:
        # Returns the first formatted address match
        return reverse_geocode_result[0]['formatted_address']
    else:
        return "No address found."

# Usage
API_KEY = 'INSERT_YOUR_API_KEY'
# Example coords from your file
lat, lng = 40.714224, -73.961452

address = get_address(lat, lng, API_KEY)
print(f"Coordinates: {lat}, {lng}")
print(f"Address: {address}")
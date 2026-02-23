import googlemaps

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
API_KEY = 'INSERT_YOUR_API_KEY'
address = "1600 Amphitheatre Parkway, Mountain View, CA"
coords = get_coords(address, API_KEY)

if coords:
    print(f"Address: {address}")
    print(f"Coordinates: Latitude {coords[0]}, Longitude {coords[1]}")
else:
    print("Address not found.")
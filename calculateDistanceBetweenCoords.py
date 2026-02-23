import math

def haversine_distance(coord1, coord2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Radius of the Earth in kilometers
    R = 6371.0 
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    km = R * c
    miles = km * 0.621371
    return km, miles

# Point 1: NYC, Point 2: LA (From your HTML example)
p1 = (40.7128, -74.0060)
p2 = (34.0522, -118.2437)

km, miles = haversine_distance(p1, p2)
print(f"Distance: {km:.2f} km ({miles:.2f} miles)")
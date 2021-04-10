from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="TrojanSafe")
location = geolocator.geocode("Jefferson bd and Flower st, Los Angeles, CA")
print(location.address)

print((location.raw.get("lat"), location.raw.get("lon")))
print(location.point)

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent = 'TrojanSafe')
#location = geolocator.geocode("1210 W Adams Blvd, LA, CA, 90007")
# print(location.address)
# print((location.latitude, location.longitude))


# PLOTTING ON MAP
# import the library and its Marker clusterization service
import folium
from folium.plugins import MarkerCluster
import pandas as pd
import io
# Create a map object and center it to the avarage coordinates to m
data = """Name,Address
home,"1210 W Adams Blvd, LA, CA, 90007"
Apple,"1 Apple Park Way, Cupertino, CA"
Google,"1600 Amphitheatre Parkway Mountain View, CA 94043"
"""
df = pd.read_csv(io.StringIO(data))
df["loc"] = df["Address"].apply(geolocator.geocode)
df["point"]= df["loc"].apply(lambda loc: tuple(loc.point) if loc else None)
df[['lat', 'lon', 'altitude']] = pd.DataFrame(df['point'].to_list(), index=df.index)

m = folium.Map(location=df[["lat", "lon"]].mean().to_list(), zoom_start=2)
# if the points are too close to each other, cluster them, create a cluster overlay with MarkerCluster, add to m
marker_cluster = MarkerCluster().add_to(m)
# draw the markers and assign popup and hover texts
# add the markers the the cluster layers so that they are automatically clustered
for i,r in df.iterrows():
    location = (r["lat"], r["lon"])
    folium.Marker(location=location,
                      popup = r['Name'],
                      tooltip=r['Name'],
                      icon= folium.Icon(color='red'))\
    .add_to(marker_cluster)
m.save('temp.html')

import folium
from folium import plugins

import osmium
#map = folium.Map(location=(50, 0), zoom_start=8)#location - the center of the map, zoom_start - the resolution
import json
import geopandas as gpd
import requests

access_token = "MLY|25204399145874923|91edfe348b19b66200b3119e41b28487"
z = 14
x = 9774
y = 6649

# Define the Mapillary tile layer URL
tile_layer_url = f'https://tiles.mapillary.com/maps/vtp/mly1_public/2/{z}/{x}/{y}?access_token={access_token}'
response = requests.get(tile_layer_url)
print(tile_layer_url)
# Check if the request was successful
if response.status_code == 200:
    # Save the content to a file
    with open('mapillary_tiles.pbf', 'wb') as f:
        f.write(response.content)
    print("PBF file saved successfully.")
else:
    print("Failed to retrieve the PBF file.")

navigation_coordinates = [0,60]
m = folium.Map(location=navigation_coordinates, zoom_start=10)

# Add navigation marker to the map
navigation_marker = folium.Marker(
    location=navigation_coordinates,
    popup=folium.Popup("Navigate here", parse_html=True),
    icon=folium.Icon(color='blue')
)
navigation_marker.add_to(m)

# vector_tile_layer = folium.plugins.TimestampedGeoJson(
#     data='mapillary_tiles.pbf',
#     period='P1M',  # Specify the time period (adjust as needed)
#     duration='P1M',  # Specify the duration (adjust as needed)
#     add_last_point=True,
#     auto_play=False,  # Set auto_play to True if you want the animation to start automatically
#     loop=False,  # Set loop to True if you want the animation to loop
#     max_speed=1,  # Specify the animation speed (adjust as needed)
# )
#
#
# # Add the vector tile layer to the map
# m.add_child(vector_tile_layer)
folium.TileLayer(tiles='mapillary_tiles.pbf',attr='trying',name='try layer',overlay=True,control=True,bounds=bounds).add_to(m)
# Add layer control to toggle layers
folium.LayerControl().add_to(m)
# Save the map
m.save('map_with_vector_tiles.html')


# Create a map object
# m = folium.Map(location=[x, y], zoom_start=10, tiles=None)
# m = folium.Map(location=[x,y], zoom_start=10)


#
# # Define the input and output file paths
# input_pbf_file = 'mapillary_tiles.pbf'
# output_geojson_file = 'mapillary_tiles.geojson'
#
# # Define a simple handler to convert OSM entities to GeoJSON
# class GeoJSONHandler(osmium.SimpleHandler):
#     def __init__(self, output_file):
#         super().__init__()
#         self.output_file = output_file
#
#     def node(self, n):
#         # Convert the OSM node to a GeoJSON feature
#         feature = {
#             "type": "Feature",
#             "geometry": {
#                 "type": "Point",
#                 "coordinates": [n.location.lon, n.location.lat]
#             },
#             "properties": {}
#         }
#         # Write the GeoJSON feature to the output file
#         self.output_file.write(feature)
#
#     # Similar methods can be implemented for ways and relations if needed
#
# # Open the output GeoJSON file in write mode
# with open(output_geojson_file, 'w') as output_file:
#     # Create an instance of the GeoJSONHandler and pass the output file
#     handler = GeoJSONHandler(output_file)
#     # Use osmium to read the PBF file and apply the handler
#     handler.apply_file(input_pbf_file, locations=True)
#
#
# # Add the Mapillary tile layer
# # Load the GeoJSON data
# geojson_data = json.load(open(output_geojson_file))
#
# # Add the GeoJSON data as a GeoJson layer
# folium.GeoJson(geojson_data).add_to(m)


# m.save('map_with_mapillary.html')

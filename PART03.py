import configurations
import folium
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the access token and bounding box
access_token = configurations.access_token
bbox = configurations.bbox

# Define the API URL
api_url = f"https://graph.mapillary.com/images?access_token={access_token}&fields=id&bbox={bbox}"

# Send GET request to the API URL
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    # Extract image IDs from the API response
    data = response.json()
    image_ids = [image['id'] for image in data['data']]

    # Create a map object
    m = folium.Map(location=[32.069, 34.769], zoom_start=15)

    # Add markers for each image ID directly to the GeoJSON layer
    for image in data['data']:
        # Construct the URL for viewing the image on Mapillary
        image_id = image['id']
        image_url = f"https://graph.mapillary.com/{image_id}?access_token={access_token}&fields=id,computed_geometry"
        response_image = requests.get(image_url)

        if response_image.status_code == 200:
            response_image = response_image.json()
            # Extract location
            if (response_image['computed_geometry']['coordinates'] != None):
                location = response_image['computed_geometry']['coordinates']

                # Add marker to the map
                marker = folium.Marker(
                    location= [location[1], location[0]],
                    popup=f"<a href='{image_url}' target='_blank'>View Image</a>"
                )
                marker.add_to(m)

                #logger success message
                logger.info(f"Added marker for image ID: {image_id} in location {location}")
            else:
                logger.error(f"image ID: {image_id} has no geometry")
    # try:
    #     folium.GeoJson(geojson_layer).add_to(m)
    # except:
    #     logger.error(f"couldn't save the layer to map as geojson")
    #     print(geojson_layer)

    # Add layer control to toggle layers
    folium.LayerControl().add_to(m)


    # Save the map
    m.save('map_with_mapillary_images.html')
    logger.info("Map saved successfully.")
else:
    logger.error("Failed to retrieve image IDs.")
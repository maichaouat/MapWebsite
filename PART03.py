import PART04
import configurations
import folium
import requests
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the API URL
api_url = configurations.mapilary_bbox_url()

# Send GET request to the API URL
response = requests.get(api_url)

# Directory to save images
image_dir = 'mapillary_images'
os.makedirs(image_dir, exist_ok=True)

# Check if the request was successful
if response.status_code == 200:
    # Extract image IDs from the API response
    data = response.json()

    # Create a map object
    m = folium.Map(location=[32.069, 34.769], zoom_start=15)

    # Add markers for each image ID directly to the GeoJSON layer
    for image in data['data']:
        image = PART04.fetch_image(image_id=image['id'])
        with open(image_dir, 'wb') as f:
            json.dump(image, f)



    folium.LayerControl().add_to(m)

    # Save the map
    m.save('map_with_mapillary_images.html')
    logger.info("Map saved successfully.")
else:
    logger.error("Failed to retrieve image IDs.")
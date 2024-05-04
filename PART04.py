from flask import Flask, request, jsonify
import folium
import requests
import configurations
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Mapillary API requestor function
def query_mapillary(bbox):
    # Construct the API endpoint URL
    api_url = f"https://graph.mapillary.com/images?access_token={configurations.access_token}&fields=id&bbox={bbox}"

    # Make the API request
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract location and image IDs from the response
        points = []
        limit = 0
        # Add markers for each image ID
        for image in data['data']:
            if limit >=10:
                break
            limit+=1
            image_id = image['id']
            image_url = f"https://graph.mapillary.com/{image_id}?access_token={configurations.access_token}&fields=id,computed_geometry,detections.value"
            response_image = requests.get(image_url)

            if response_image.status_code == 200:
                response_image = response_image.json()
                # Extract location
                if response_image['computed_geometry']['coordinates'] is not None:
                    location = response_image['computed_geometry']['coordinates']
                    points.append({'location': [location[1], location[0]], 'image_id': image_id, 'image_url':image_url})
                    # logger success message
                    logger.info(f"Added point for image ID: {image_id} in location {location}")
                else:
                    logger.error(f"Image ID: {image_id} has no geometry")

        return points
    else:
        logger.error(f"Request failed with status code {response.status_code}")
        return None

@app.route('/moved', methods=['POST'])
def map_moved():
    data = request.get_json()
    bbox = data['bbox']
    points = query_mapillary(bbox)
    if points:
        return jsonify(points)
    else:
        return jsonify([])

@app.route('/')
def index():
    # Return the content of the map.html file
    with open('map.html', 'r') as f:
        map_html = f.read()
    return map_html

if __name__ == '__main__':
    app.run(debug=True)

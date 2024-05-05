from flask import Flask, request, jsonify
import folium
import requests
import configurations
import logging
from concurrent.futures import ThreadPoolExecutor

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

        with ThreadPoolExecutor() as executor:
            for image in data['data']:
                image_result = executor.submit(fetch_image, image).result()
                points.append(image_result)
                limit += 1
                if limit >= 2:
                    break
        return points
    else:
        logger.error(f"Request failed with status code {response.status_code}")
        return None


def fetch_image(image):
    image_id = image['id']
    image_url = f"https://graph.mapillary.com/{image_id}?access_token={configurations.access_token}&fields=id,computed_geometry,detections.value"
    response = requests.get(image_url)
    if response.status_code == 200:
        response_json = response.json()
        if 'computed_geometry' in response_json:
            location = response_json['computed_geometry']['coordinates']
            return {'location': [location[1], location[0]], 'image_id': image_id}
        else:
            logger.error(f"Image ID: {image_id} has no geometry")
            return None
    else:
        logger.error(f"Failed to fetch image data for ID: {image_id}")
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


@app.route('/get_image_data', methods=['GET'])
def get_image_data():
    # Get the Image ID from the request parameters
    image_id = request.args.get('image_id')

    # Make a request to fetch image parameters
    response = requests.get(configurations.mapilary_image_parameters(image_id))

    if response.status_code == 200:
        # Extract image parameters from the response
        image_params = response.json()


        # Define metadata and insert all data there
        metadata = {
            'image_id': image_id,
            'metadata': image_params,
            'url' : configurations.mapillary_image_url(image_id),
            'timestamp': image_params.get('timestamp', None),  # Example, extract timestamp if available
            # Add more metadata fields as needed
        }

        # Return metadata as JSON response
        return jsonify(metadata)
    else:
        # If image not found, return error response
        return jsonify({'error': 'Image not found'}), response.status_code

@app.route('/')
def index():
    # Return the content of the map.html file
    with open('map.html', 'r') as f:
        map_html = f.read()
    return map_html

if __name__ == '__main__':
    app.run(debug=True)

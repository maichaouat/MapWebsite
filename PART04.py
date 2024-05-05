from flask import Flask, request, jsonify
import folium
import requests
import configurations
import logging
from concurrent.futures import ThreadPoolExecutor
from flask_caching import Cache
from flask import render_template

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask-Caching
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache_ids = Cache(config={'CACHE_TYPE': 'SimpleCache'})

app = Flask(__name__)
cache.init_app(app)
cache_ids.init_app(app)

# Mapillary API requestor function
def query_mapillary(bbox=None, max_retrive =10):
    # Construct the API endpoint URL
    if bbox:
        api_url = configurations.mapilary_bbox_url(bbox)
    else: #Get initial bbox (as default)
        api_url = configurations.mapilary_bbox_url()

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
                image_result = executor.submit(fetch_image, image['id']).result()
                points.append(image_result)
                limit += 1
                if limit >= max_retrive:
                    break
        return points
    else:
        logger.error(f"Request failed with status code {response.status_code}")
        return None


@cache.memoize(timeout=600)
def fetch_image(image_id):
    image_url = configurations.mapilary_image_with_location(image_id)
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
@cache_ids.memoize(timeout=600)
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
    points = query_mapillary(max_retrive=100)  # Assuming you have a function to fetch points data
    logger.info("Succeeded to load the images from the start bbox")
    return render_template('map.html', points=points)

if __name__ == '__main__':
    app.run(debug=True)

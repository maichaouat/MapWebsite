import requests


# Define the access token and bounding box
access_token = "MLY|25204399145874923|91edfe348b19b66200b3119e41b28487"
bbox = "34.768,32.068,34.770,32.070"  # Provided bounding box

# Define the API URL
api_url = f"https://graph.mapillary.com/images?access_token={access_token}&fields=id&bbox={bbox}"

def mapillary_image_url(image_id):
    return f"https://www.mapillary.com/app/?focus=photo&pKey={image_id}"


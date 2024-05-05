
# Define the access token and bounding box
access_token = "MLY|25204399145874923|91edfe348b19b66200b3119e41b28487"
bbox = "34.768,32.068,34.770,32.070"  # Provided bounding box

# Define the API URL
def mapilary_bbox_url(bbox = bbox):
    return f"https://graph.mapillary.com/images?access_token={access_token}&fields=id&bbox={bbox}"

def mapillary_image_url(image_id):
    return f"https://www.mapillary.com/app/?focus=photo&pKey={image_id}"

def mapilary_image_parameters(image_id):
    return f"https://graph.mapillary.com/{image_id}?access_token={access_token}&fields=id,computed_geometry"

def mapilary_image_with_location(image_id):
    return f"https://graph.mapillary.com/{image_id}?access_token={access_token}&fields=id,computed_geometry"


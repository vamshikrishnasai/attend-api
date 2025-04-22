from flask import Flask, request, jsonify, abort
from pyzbar.pyzbar import decode
import cv2
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Helper function to check if the file is a valid image type
def is_valid_image(file):
    allowed_mime_types = ['image/jpeg', 'image/png']
    if file.content_type not in allowed_mime_types:
        return False
    return True

@app.route('/scan-barcode', methods=['POST'])
def scan_barcode():
    # Get image from request
    file = request.files.get('image')
    if not file:
        abort(400, description="No image provided")

    # Validate the file type
    if not is_valid_image(file):
        abort(400, description="Invalid file type. Only JPEG and PNG are allowed.")
    
    # Convert image to format suitable for pyzbar
    nparr = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        abort(400, description="Failed to decode image")

    # Decode barcode(s)
    decoded_objects = decode(image)
    
    if not decoded_objects:
        abort(400, description="No barcode found")

    # Extract barcode data from decoded objects
    decoded_data = [obj.data.decode('utf-8') for obj in decoded_objects]

    # Return barcode data with a timestamp
    response = {
        'data': decoded_data,  # List of decoded barcodes
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

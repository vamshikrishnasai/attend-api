from flask import Flask, request, jsonify
from pyzbar.pyzbar import decode
import cv2
import numpy as np
from datetime import datetime

app = Flask(__name__)

@app.route('/scan-barcode', methods=['POST'])
def scan_barcode():
    # Get image from request
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    # Convert image to format suitable for pyzbar
    nparr = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Decode barcode
    decoded_objects = decode(image)
    
    if not decoded_objects:
        return jsonify({'error': 'No barcode found'}), 400
    
    # Get first decoded barcode data
    barcode_data = decoded_objects[0].data.decode('utf-8')
    
    response = {
        'data': barcode_data,
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

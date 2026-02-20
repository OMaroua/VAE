"""
Flask web application for VAE model inference.
Allows users to upload images and get processed outputs.
"""

import os
import io
from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from model_utils import load_model, preprocess_image, postprocess_image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Global model variable (loaded on startup)
model = None


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image upload and process through VAE model."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, TIFF'}), 400
    
    try:
        # Read image
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Image will be converted to grayscale in preprocess_image
        
        # Preprocess image
        input_array = preprocess_image(image)
        
        # Run inference
        output = model.predict(input_array, verbose=0)
        
        # If model returns a list/tuple, take first element
        if isinstance(output, (list, tuple)):
            output_array = output[0]
        else:
            output_array = output
        
        # Postprocess output
        output_image = postprocess_image(output_array)
        
        # Save output image to bytes
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='PNG')
        output_buffer.seek(0)
        
        return send_file(
            output_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name='output.png'
        )
    
    except Exception as e:
        return jsonify({'error': f'Processing error: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    import tensorflow as tf
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'tensorflow_version': tf.__version__,
        'gpu_available': len(tf.config.list_physical_devices('GPU')) > 0
    })


def init_model():
    """Initialize and load the Keras model."""
    global model
    try:
        model = load_model()
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please ensure the model file exists at models/denoiser.keras")


if __name__ == '__main__':
    print("Initializing model...")
    init_model()
    print("Starting Flask server...")
    # Use port 5001 if 5000 is occupied (common on macOS due to AirPlay)
    import socket
    port = 5000
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', 5000))
        sock.close()
    except OSError:
        port = 5001
        print("Port 5000 is in use, using port 5001 instead")
    print(f"Server starting on http://0.0.0.0:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)


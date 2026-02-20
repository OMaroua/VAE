# VAE Model Web Interface

A web-based interface for running inference on trained VAE (Variational Autoencoder) models. Users can upload images and receive processed outputs automatically.

## Features

- **Image Upload**: Drag-and-drop or click to upload images
- **Real-time Processing**: Process images through your trained VAE model
- **Download Results**: Download processed images
- **Modern UI**: Clean, responsive web interface
- **One Image at a Time**: Processes single images as required

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Place Your Model File

The application is configured to load the Keras model from `models/denoiser.keras`. Ensure your model file is located at:
```
models/denoiser.keras
```

If your model is in a different location, update `MODEL_PATH` in `model_utils.py`:
```python
MODEL_PATH = 'path/to/your/model.keras'
```

### 3. Adjust Preprocessing (Optional)

If your model was trained with different preprocessing (e.g., different normalization, image size), you may need to modify `preprocess_image()` in `model_utils.py` to match your training setup.

### 4. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 5. Access the Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. **Upload Image**: Click the upload area or drag and drop an image
2. **Process**: Click "Process Image" to run inference
3. **View Results**: See both input and output images side by side
4. **Download**: Click "Download Result" to save the processed image

## File Structure

```
VAE/
├── app.py                 # Flask application
├── model_utils.py         # Model loading and preprocessing utilities
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary upload storage (auto-created)
└── outputs/              # Output storage (auto-created)
```

## API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload and process image
- `GET /health` - Health check endpoint

## Customization

### Changing Port

Edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### Adjusting File Size Limit

Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Supported Image Formats

Currently supports: PNG, JPG, JPEG, GIF, BMP, TIFF

To add more formats, update `ALLOWED_EXTENSIONS` in `app.py`.

## Troubleshooting

### Model Not Loading

- Check that `MODEL_PATH` points to the correct file (`models/denoiser.keras`)
- Ensure the model file is a valid Keras model (`.keras` format)
- Verify TensorFlow version is compatible (2.13.0 or higher)

### Image Processing Errors

- Verify image preprocessing matches training preprocessing
- Check that input image dimensions are compatible with your model
- Ensure images are normalized the same way as during training

### GPU/CPU Issues

The application automatically uses GPU if available. TensorFlow will use GPU by default if CUDA is properly configured. To force CPU-only mode, set:
```bash
export CUDA_VISIBLE_DEVICES=""
```
before running the application.

## Production Deployment

For production use, consider:

1. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Add authentication** if needed

3. **Set up proper logging**

4. **Use environment variables** for configuration

5. **Add rate limiting** to prevent abuse

6. **Deploy on cloud platforms** (AWS, Google Cloud, Azure, etc.)

## Notes

- This interface processes multiple images at a time as specified
- Images are processed in memory and downloaded as a zip file
- The model is loaded once at startup for efficiency





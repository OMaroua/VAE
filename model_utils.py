"""
Model loading and image preprocessing utilities for Keras/TensorFlow models.
"""

import os
import numpy as np
from PIL import Image
import tensorflow as tf

# Try to use standalone Keras 3 first (as used in the notebook), fall back to TensorFlow Keras
try:
    import keras
    from keras import layers
    # Check if it's standalone Keras 3
    if hasattr(keras, 'saving'):
        USE_STANDALONE_KERAS = True
    else:
        from tensorflow import keras
        from tensorflow.keras import layers
        USE_STANDALONE_KERAS = False
except ImportError:
    from tensorflow import keras
    from tensorflow.keras import layers
    USE_STANDALONE_KERAS = False


# Custom Sampling layer for VAE (reparameterization trick)
# This matches the implementation from the notebook
class Sampling(layers.Layer):
    """Uses (z_mean, z_log_var) to sample z, the vector encoding a digit."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if USE_STANDALONE_KERAS:
            # For standalone Keras 3 (as in the notebook)
            self.seed_generator = keras.random.SeedGenerator(1337)
        else:
            # For TensorFlow Keras
            self.seed_generator = tf.random.Generator.from_seed(1337)
    
    def call(self, inputs):
        z_mean, z_log_var = inputs
        
        if USE_STANDALONE_KERAS:
            # Keras 3 API (matches notebook exactly)
            from keras import ops
            batch = ops.shape(z_mean)[0]
            dim = ops.shape(z_mean)[1]
            epsilon = keras.random.normal(shape=(batch, dim), seed=self.seed_generator)
            return z_mean + ops.exp(0.5 * z_log_var) * epsilon
        else:
            # TensorFlow API
            batch = tf.shape(z_mean)[0]
            dim = tf.shape(z_mean)[1]
            epsilon = self.seed_generator.normal(shape=(batch, dim))
            return z_mean + tf.exp(0.5 * z_log_var) * epsilon
    
    def get_config(self):
        config = super().get_config()
        return config


def load_model(device=None):
    """
    Load the trained Keras model.
    
    Args:
        device: Not used for Keras (kept for compatibility)
        
    Returns:
        Loaded Keras model
    """
    MODEL_PATH = 'models/denoiser.keras'
    
    # Check if model file exists
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH}. "
            "Please ensure the model file exists in the models/ directory."
        )
    
    # Load the Keras model with custom objects
    try:
        custom_objects = {'Sampling': Sampling}
        model = keras.models.load_model(MODEL_PATH, custom_objects=custom_objects)
        print(f"Model loaded successfully from {MODEL_PATH}")
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading model: {e}")


def preprocess_image(image, image_size=28):
    """
    Preprocess image for model input.
    
    The model expects 28x28 grayscale images based on the error message.
    
    Args:
        image: PIL Image
        image_size: Target size for resizing (default: 28 for this model)
        
    Returns:
        Preprocessed numpy array ready for model input
    """
    # Convert to grayscale (L mode)
    if image.mode != 'L':
        image = image.convert('L')
    
    # Resize to model input size (28x28)
    image = image.resize((image_size, image_size), Image.Resampling.LANCZOS)
    
    # Convert PIL to numpy array
    img_array = np.array(image, dtype=np.float32)
    
    # Normalize to [0, 1] range
    img_array = img_array / 255.0
    
    # Add channel dimension: (height, width) -> (height, width, 1)
    img_array = np.expand_dims(img_array, axis=-1)
    
    # Add batch dimension: (height, width, channels) -> (1, height, width, channels)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def postprocess_image(output_array):
    """
    Postprocess model output array to PIL Image.
    
    Args:
        output_array: Model output numpy array (batch, height, width, channels) or (height, width, channels)
        
    Returns:
        PIL Image (grayscale)
    """
    # Remove batch dimension if present
    if len(output_array.shape) == 4:
        output_array = output_array[0]
    
    # If it has a channel dimension and it's 1, squeeze it
    if len(output_array.shape) == 3 and output_array.shape[2] == 1:
        output_array = np.squeeze(output_array, axis=2)
    
    # Ensure values are in [0, 1] range
    output_array = np.clip(output_array, 0, 1)
    
    # Convert to uint8
    output_array = (output_array * 255).astype(np.uint8)
    
    # Convert to PIL Image (grayscale)
    image = Image.fromarray(output_array, mode='L')
    
    return image


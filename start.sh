#!/bin/bash
# Production startup script for VAE Denoising Interface

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Start Gunicorn server
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 --access-logfile - --error-logfile - app:app


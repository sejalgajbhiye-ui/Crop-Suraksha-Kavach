# Backend

The backend provides a Flask API that connects the ESP32-CAM with the YOLOv8 detection model.

## API

### GET /
Returns project and model information.

### GET /health
Checks whether the backend is running.

### POST /detect
Accepts an image and performs animal detection.

## Detection Pipeline

Image
↓
Flask API
↓
YOLOv8
↓
Animal + Confidence + Bounding Box
↓
Alert Generation
import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    from backend.config import SERVER_HOST, SERVER_PORT, UPLOAD_DIR, CONFIDENCE_THRESHOLD, MODEL_CLASSES
    from backend.detector import detect_animal, model
    from backend.alert import generate_alert
except ImportError:
    from config import SERVER_HOST, SERVER_PORT, UPLOAD_DIR, CONFIDENCE_THRESHOLD, MODEL_CLASSES
    from detector import detect_animal, model
    from alert import generate_alert

app = Flask(__name__)
CORS(app)

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "Crop Suraksha Kavach API",
        "status": "online",
        "version": "1.0.0",
        "endpoints": {
            "/": "Project and model information (GET)",
            "/health": "Backend health status (GET)",
            "/detect": "Animal detection API (POST)"
        },
        "supported_classes": list(MODEL_CLASSES.values()) if isinstance(MODEL_CLASSES, dict) else MODEL_CLASSES
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })


@app.route("/detect", methods=["POST"])
def detect():
    # Check whether image was uploaded via multipart/form-data
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "message": "No image provided in request."
        }), 400

    image = request.files["image"]

    if not image or image.filename == "":
        return jsonify({
            "success": False,
            "message": "No image selected for processing."
        }), 400

    # Generate a unique filename to avoid collision
    extension = os.path.splitext(image.filename)[1] or ".jpg"
    unique_filename = f"{uuid.uuid4().hex}{extension}"
    image_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        image.save(image_path)

        # Run YOLO detection
        detections = detect_animal(image_path)

        # Generate alerts
        alerts = []
        for detection in detections:
            animal = detection["animal"]
            confidence_val = detection.get("confidence")
            alert = generate_alert(animal, confidence=confidence_val)
            alerts.append(alert)

        response = {
            "success": True,
            "detections": detections,
            "alerts": alerts,
            "total_detected": len(detections)
        }

        return jsonify(response), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:
        # Delete temporary uploaded image after processing
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass


if __name__ == "__main__":
    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=True
    )
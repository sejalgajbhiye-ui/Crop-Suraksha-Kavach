import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

try:
    from backend.config import BASE_DIR, SERVER_HOST, SERVER_PORT, UPLOAD_DIR, CONFIDENCE_THRESHOLD, MODEL_CLASSES
    from backend.detector import detect_animal, model
    from backend.alert import generate_alert
except ImportError:
    from config import BASE_DIR, SERVER_HOST, SERVER_PORT, UPLOAD_DIR, CONFIDENCE_THRESHOLD, MODEL_CLASSES
    from detector import detect_animal, model
    from alert import generate_alert

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    if request.accept_mimetypes.accept_html and os.path.exists(os.path.join(FRONTEND_DIR, "index.html")):
        return send_from_directory(FRONTEND_DIR, "index.html")
    return jsonify({
        "name": "Crop Suraksha Kavach API",
        "status": "online",
        "version": "1.0.0",
        "endpoints": {
            "/": "Web Dashboard or API Information (GET)",
            "/health": "Backend health status (GET)",
            "/detect": "Animal detection API (POST)"
        },
        "supported_classes": list(MODEL_CLASSES.values()) if isinstance(MODEL_CLASSES, dict) else MODEL_CLASSES
    })


@app.route("/<path:filename>", methods=["GET"])
def serve_static(filename):
    if os.path.exists(os.path.join(FRONTEND_DIR, filename)):
        return send_from_directory(FRONTEND_DIR, filename)
    return jsonify({"error": "File not found"}), 404


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

    file = request.files["image"]
    if not file or file.filename == "":
        return jsonify({
            "success": False,
            "message": "No image selected for processing."
        }), 400

    try:
        from PIL import Image
        pil_img = Image.open(file.stream).convert("RGB")

        # Run YOLO detection in-memory
        detections = detect_animal(pil_img)

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


if __name__ == "__main__":
    app.run(
        host=SERVER_HOST,
        port=SERVER_PORT,
        debug=True
    )
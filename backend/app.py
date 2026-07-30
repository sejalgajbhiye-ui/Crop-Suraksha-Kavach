from flask import Flask, request, jsonify
from detector import detect_animal
from alert import generate_alert

import os
import uuid


app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():

    return jsonify({
        "project": "Crop Suraksha Kavach",
        "status": "running",
        "model": "YOLOv8",
        "classes": [
            "cow",
            "deer",
            "elephant"
        ]
    })


@app.route("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


@app.route("/detect", methods=["POST"])
def detect():

    if "image" not in request.files:

        return jsonify({
            "success": False,
            "message": "Image not provided"
        }), 400

    image = request.files["image"]

    filename = str(uuid.uuid4()) + ".jpg"

    image_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    image.save(image_path)

    detections = detect_animal(image_path)

    alerts = []

    for detection in detections:

        alert = generate_alert(
            detection["animal"],
            detection["confidence"]
        )

        alerts.append(alert)

    return jsonify({
        "success": True,
        "detections": detections,
        "alerts": alerts
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
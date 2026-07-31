from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
import os

app = Flask(__name__)
CORS(app)

# Load trained YOLO model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml_model",
    "weights",
    "best.pt"
)

model = YOLO(MODEL_PATH)

# Alert configuration
ALERT_CONFIG = {
    "cow": {
        "severity": "LOW",
        "message": "Cow detected."
    },
    "deer": {
        "severity": "MEDIUM",
        "message": "Deer detected! Stay alert."
    },
    "elephant": {
        "severity": "HIGH",
        "message": "Elephant detected! Take immediate action."
    }
}


def generate_alert(animal):
    """
    Generate an alert based on detected animal.
    """

    config = ALERT_CONFIG.get(
        animal,
        {
            "severity": "UNKNOWN",
            "message": f"{animal} detected."
        }
    )

    return {
        "animal": animal,
        "severity": config["severity"],
        "message": config["message"]
    }


def detect_animal(image_path):
    """
    Run YOLO detection on the received image.
    """

    results = model.predict(
        source=image_path,
        imgsz=640,
        conf=0.5,
        verbose=False
    )

    detections = []

    for result in results:

        boxes = result.boxes

        for box in boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            animal = model.names[class_id]

            # YOLO bounding box:
            # x1, y1, x2, y2
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "animal": animal,
                "confidence": round(confidence, 2),
                "bounding_box": [
                    round(x1),
                    round(y1),
                    round(x2),
                    round(y2)
                ]
            })

    return detections


@app.route("/detect", methods=["POST"])
def detect():

    # Check whether image was uploaded
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "message": "No image provided."
        }), 400

    image = request.files["image"]

    if image.filename == "":
        return jsonify({
            "success": False,
            "message": "No image selected."
        }), 400

    # Temporary upload directory
    upload_dir = "/tmp/uploads"

    os.makedirs(upload_dir, exist_ok=True)

    image_path = os.path.join(
        upload_dir,
        image.filename
    )

    image.save(image_path)

    try:

        # Run YOLO
        detections = detect_animal(image_path)

        # Generate alerts
        alerts = []

        for detection in detections:

            animal = detection["animal"]

            alert = generate_alert(animal)

            alerts.append(alert)

        response = {
            "success": True,
            "detections": detections,
            "alerts": alerts
        }

        return jsonify(response)

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

    finally:

        # Delete uploaded image after processing
        if os.path.exists(image_path):
            os.remove(image_path)


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "Crop Suraksha Kavach backend running",
        "endpoint": "/detect"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
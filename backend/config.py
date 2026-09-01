import os
import tempfile

# Prevent Ultralytics from writing to read-only directories on cloud containers
os.environ["YOLO_CONFIG_DIR"] = tempfile.gettempdir()
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["TORCH_NUM_THREADS"] = "1"

# Server Configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

# Base Directories and Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "ml_model", "weights", "best.pt")
FALLBACK_MODEL_PATH = os.path.join(BASE_DIR, "yolov8n.pt")

# Temporary Upload Directory (cross-platform safe)
UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "crop_suraksha_uploads")

# Model Detection Settings
CONFIDENCE_THRESHOLD = 0.25
IMAGE_SIZE = 320

MODEL_CLASSES = {
    0: "cow",
    1: "deer",
    2: "elephant"
}

# Alert Configuration by Animal
ALERT_CONFIG = {
    "cow": {
        "severity": "LOW",
        "message": "Cow detected in the monitoring zone.",
        "buzzer": True,
        "led": True,
        "gsm": False
    },
    "deer": {
        "severity": "MEDIUM",
        "message": "Deer detected! Stay alert.",
        "buzzer": True,
        "led": True,
        "gsm": True
    },
    "elephant": {
        "severity": "HIGH",
        "message": "Elephant detected! Take immediate action.",
        "buzzer": True,
        "led": True,
        "gsm": True
    }
}
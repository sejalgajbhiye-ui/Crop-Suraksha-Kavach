import os
import numpy as np
import torch
from ultralytics import YOLO

try:
    from backend.config import MODEL_PATH, FALLBACK_MODEL_PATH, CONFIDENCE_THRESHOLD, IMAGE_SIZE, MODEL_CLASSES
except ImportError:
    from config import MODEL_PATH, FALLBACK_MODEL_PATH, CONFIDENCE_THRESHOLD, IMAGE_SIZE, MODEL_CLASSES

# Optimize thread usage for cloud containers
torch.set_num_threads(2)

# Initialize YOLO model
selected_model_path = MODEL_PATH if os.path.exists(MODEL_PATH) else FALLBACK_MODEL_PATH
if not os.path.exists(selected_model_path):
    raise FileNotFoundError(f"YOLO model weights not found at {MODEL_PATH} or {FALLBACK_MODEL_PATH}")

model = YOLO(selected_model_path)

# Warm up model on server startup to eliminate cold-start latency on first request
try:
    _dummy = np.zeros((320, 320, 3), dtype=np.uint8)
    model.predict(source=_dummy, imgsz=320, device="cpu", verbose=False)
    print("YOLO model initialized and warmed up successfully.")
except Exception as _e:
    print(f"Model warmup notice: {_e}")


@torch.inference_mode()
def detect_animal(image_path, conf_threshold=CONFIDENCE_THRESHOLD):
    """
    Run YOLO detection on the input image and return parsed animal detections.
    """
    results = model.predict(
        source=image_path,
        imgsz=IMAGE_SIZE,
        conf=conf_threshold,
        device="cpu",
        verbose=False
    )

    detections = []

    for result in results:
        if result.boxes is None or len(result.boxes) == 0:
            continue

        for box in result.boxes:
            class_id = int(box.cls[0].item() if hasattr(box.cls[0], "item") else box.cls[0])
            confidence = float(box.conf[0].item() if hasattr(box.conf[0], "item") else box.conf[0])

            # Try to get class name from model names or fallback dict
            if hasattr(model, "names") and class_id in model.names:
                animal = model.names[class_id]
            else:
                animal = MODEL_CLASSES.get(class_id, "unknown")

            # YOLO bounding box: x1, y1, x2, y2
            xyxy = box.xyxy[0].tolist()
            x1, y1, x2, y2 = xyxy

            detections.append({
                "animal": str(animal).lower(),
                "confidence": round(confidence, 3),
                "bounding_box": [
                    round(x1, 2),
                    round(y1, 2),
                    round(x2, 2),
                    round(y2, 2)
                ]
            })

    return detections

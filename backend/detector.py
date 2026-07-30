from ultralytics import YOLO
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "ml_model",
    "weights",
    "best.pt"
)

model = YOLO(MODEL_PATH)

CLASS_NAMES = {
    0: "cow",
    1: "deer",
    2: "elephant"
}


def detect_animal(image_path):

    results = model.predict(
        source=image_path,
        imgsz=640,
        conf=0.5,
        device="cpu",
        verbose=False
    )

    detections = []

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            animal = CLASS_NAMES.get(
                class_id,
                "unknown"
            )

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detections.append({
                "animal": animal,
                "confidence": round(confidence, 3),
                "bounding_box": [
                    round(x1, 2),
                    round(y1, 2),
                    round(x2, 2),
                    round(y2, 2)
                ]
            })

    return detections
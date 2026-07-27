import os
import shutil
import yaml
import fiftyone.zoo as foz

from fiftyone import ViewField as F

# -------------------------------
# Create folders
# -------------------------------

OUTPUT_DIR = "dataset/yolo_dataset"

IMAGE_DIR = os.path.join(OUTPUT_DIR, "images", "train")
LABEL_DIR = os.path.join(OUTPUT_DIR, "labels", "train")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(LABEL_DIR, exist_ok=True)

# -------------------------------
# Load dataset
# -------------------------------

dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections"],
    classes=["Cattle", "Deer", "Elephant"],
    max_samples=3000,
)

print("Dataset loaded.")

# -------------------------------
# Class Mapping
# -------------------------------

CLASS_MAP = {
    "Cattle": 0,
    "Deer": 1,
    "Elephant": 2,
}

CLASS_NAME = {
    "Cattle": "cow",
    "Deer": "deer",
    "Elephant": "elephant",
}

# -------------------------------
# Export all images and labels
# -------------------------------

count = 0

for sample in dataset:

    # Copy image
    image_name = os.path.basename(sample.filepath)
    destination = os.path.join(IMAGE_DIR, image_name)

    if not os.path.exists(destination):
        shutil.copy(sample.filepath, destination)

    # Create label file
    label_name = os.path.splitext(image_name)[0] + ".txt"
    label_path = os.path.join(LABEL_DIR, label_name)

    with open(label_path, "w") as f:

        if sample.ground_truth is None:
            continue

        for detection in sample.ground_truth.detections:

            if detection.label not in CLASS_MAP:
                continue

            class_id = CLASS_MAP[detection.label]

            x, y, w, h = detection.bounding_box

            x_center = x + w / 2
            y_center = y + h / 2

            f.write(
                f"{class_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n"
            )

    count += 1

print(f"\nProcessed {count} images successfully!")
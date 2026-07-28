import fiftyone.zoo as foz
import fiftyone.types as fot
import os
import shutil

# Remove old export if it exists
if os.path.exists("dataset/yolo_dataset"):
    shutil.rmtree("dataset/yolo_dataset")

# Load dataset
dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections"],
    classes=["Cattle", "Deer", "Elephant"],
    max_samples=3000,
)

print("Dataset loaded!")

# Export
dataset.export(
    export_dir="dataset/yolo_dataset",
    dataset_type=fot.YOLOv5Dataset,
    label_field="ground_truth",
)

print("YOLO dataset exported successfully!")
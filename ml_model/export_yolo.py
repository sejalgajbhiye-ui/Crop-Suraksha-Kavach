import fiftyone.zoo as foz
from fiftyone.types import YOLOv5Dataset

# Load the dataset
dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections"],
    classes=["Cattle", "Deer", "Elephant"],
    max_samples=3000,
)

# Export in YOLO format
dataset.export(
    export_dir="dataset/yolo_dataset",
    dataset_type=YOLOv5Dataset,
    label_field="ground_truth",   # <-- Changed from detections
)

print("YOLO dataset exported successfully!")
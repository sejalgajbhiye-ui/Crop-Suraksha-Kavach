import fiftyone.zoo as foz
import os
import shutil
import random

dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections"],
    classes=["Cattle", "Deer", "Elephant"],
    max_samples=3000,
)

print(f"Loaded {len(dataset)} images")

OUTPUT = "dataset"

if os.path.exists(OUTPUT):
    shutil.rmtree(OUTPUT)

splits = ["train", "valid", "test"]

for split in splits:
    os.makedirs(f"{OUTPUT}/{split}/images", exist_ok=True)
    os.makedirs(f"{OUTPUT}/{split}/labels", exist_ok=True)

print("Folders created!")

samples = list(dataset)

random.seed(42)
random.shuffle(samples)

total = len(samples)

train_end = int(0.7 * total)
valid_end = int(0.9 * total)

train_samples = samples[:train_end]
valid_samples = samples[train_end:valid_end]
test_samples = samples[valid_end:]

print(len(train_samples))
print(len(valid_samples))
print(len(test_samples))

from pathlib import Path

CLASS_MAP = {
    "Cattle": 0,
    "Deer": 1,
    "Elephant": 2,
}

CLASS_NAMES = ["cow", "deer", "elephant"]


def export_split(samples, split_name):
    image_dir = Path(f"dataset/{split_name}/images")
    label_dir = Path(f"dataset/{split_name}/labels")

    exported = 0

    for sample in samples:

        # Copy image
        image_path = Path(sample.filepath)
        shutil.copy(image_path, image_dir / image_path.name)

        # Create label file
        label_file = label_dir / (image_path.stem + ".txt")

        with open(label_file, "w") as f:

            detections = sample.ground_truth.detections

            for det in detections:

                if det.label not in CLASS_MAP:
                    continue

                class_id = CLASS_MAP[det.label]

                x, y, w, h = det.bounding_box

                # Convert to YOLO format
                x_center = x + w / 2
                y_center = y + h / 2

                f.write(
                    f"{class_id} "
                    f"{x_center:.6f} "
                    f"{y_center:.6f} "
                    f"{w:.6f} "
                    f"{h:.6f}\n"
                )

        exported += 1

    print(f"{split_name}: {exported} images exported")

export_split(train_samples, "train")
export_split(valid_samples, "valid")
export_split(test_samples, "test")

print("Images and labels exported successfully!")


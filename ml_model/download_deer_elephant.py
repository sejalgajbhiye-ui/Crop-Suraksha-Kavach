import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset(
    "open-images-v7",
    split="train",
    label_types=["detections"],
    classes=["Deer", "Elephant"],
    max_samples=2000,
)

print("Download completed!")
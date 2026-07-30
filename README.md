# Crop Suraksha Kavach 🌾🛡️

An intelligent animal detection and farmer alert system designed to help protect agricultural fields from potentially dangerous animal intrusions.

The system uses an ESP32-CAM to capture images, a Flask backend to process the images, and a custom-trained YOLOv8 object detection model to identify animals.

The current ML model detects:

- Cow
- Deer
- Elephant

---

## Project Overview

Farmers working near forest regions can face crop damage and safety risks due to animal intrusion.

Crop Suraksha Kavach aims to provide an automated detection and alert mechanism that detects animals entering agricultural areas and generates alerts for the farmer.

### System Workflow

ESP32-CAM
    ↓
Capture Image
    ↓
Send Image to Flask Backend
    ↓
YOLOv8 Object Detection
    ↓
Cow / Deer / Elephant Detection
    ↓
Generate Alert
    ↓
Notify Farmer


---

## Features

- YOLOv8-based animal detection
- Detection of Cow, Deer and Elephant
- Bounding-box based object detection
- Confidence score for detected objects
- ESP32-CAM based image capture
- Flask REST API for image processing
- Automated alert generation
- Buzzer and LED alert interface
- GSM alert interface
- Modular ML, backend and hardware architecture


---

## Machine Learning

### Model

The project uses YOLOv8n as the base object detection architecture.

The custom-trained model detects three classes:

0 → cow
1 → deer
2 → elephant

The final trained model is stored at:

ml_model/
└── weights/
    └── best.pt


### Dataset

The dataset was prepared using FiftyOne and the Open Images V7 dataset.

The required classes were selected from Open Images:

- Cattle
- Deer
- Elephant

The Cattle class was renamed to:

Cattle → cow

Other classes present in the original dataset, such as Goat, Sheep, Person, Car, etc., were ignored.

---

## Dataset Preparation Pipeline

Open Images V7
        ↓
FiftyOne
        ↓
Select required classes
        ↓
Cattle
Deer
Elephant
        ↓
Rename Cattle → cow
        ↓
Convert bounding boxes to YOLO format
        ↓
3000 images
        ↓
Train / Validation / Test split
        ↓
YOLOv8 Training


### Dataset Split

| Dataset | Images |
|---------|-------:|
| Training | 2100 |
| Validation | 600 |
| Testing | 300 |
| Total | 3000 |

The dataset images and labels are not stored in GitHub because of their large size.

The dataset configuration is stored in:

dataset/data.yaml


---

## Project Structure

Crop-Suraksha-Kavach/
│
├── backend/
│   ├── alert.py
│   ├── app.py
│   ├── config.py
│   ├── detector.py
│   └── requirements.txt
│
├── dataset/
│   └── data.yaml
│
├── docs/
│
├── hardware/
│   └── esp32_cam/
│       └── esp32_cam.ino
│
├── ml_model/
│   ├── weights/
│   │   └── best.pt
│   │
│   ├── custom_export_yolo.py
│   ├── download_cattle.py
│   ├── download_dataset.py
│   ├── download_deer_elephant.py
│   ├── predict.py
│   └── train.py
│
├── test_images/
│   ├── cow.jpg
│   ├── deer.jpg
│   └── elephant.jpg
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt


Note: Training, validation and test images are excluded from GitHub because of their size.


---

## Model Training

The model was trained using:

- Python 3.12.4
- Ultralytics YOLO
- PyTorch
- FiftyOne
- Open Images V7

Example training command:

yolo detect train data=dataset/data.yaml model=yolov8n.pt epochs=50 imgsz=640 batch=8 device=cpu

The trained model is generated at:

runs/detect/<training-run>/weights/best.pt

The final model used for inference is stored at:

ml_model/weights/best.pt


---

## Model Evaluation

The final YOLOv8 model was evaluated on the independent test set containing 300 images.

### Overall Results

| Metric | Score |
|--------|------:|
| Precision | 0.845 |
| Recall | 0.671 |
| mAP@50 | 0.776 |
| mAP@50-95 | 0.526 |

### Per-Class Results

| Class | Precision | Recall | mAP@50 | mAP@50-95 |
|-------|----------:|-------:|--------:|----------:|
| Cow | 0.808 | 0.574 | 0.689 | 0.422 |
| Deer | 0.837 | 0.693 | 0.787 | 0.579 |
| Elephant | 0.890 | 0.747 | 0.853 | 0.576 |
| Overall | 0.845 | 0.671 | 0.776 | 0.526 |

These results were obtained by evaluating the trained YOLOv8 model on the project's test dataset.


---

## Prediction Testing

The trained model was also tested on separate sample images.

Test images:

test_images/
├── cow.jpg
├── deer.jpg
└── elephant.jpg

The model successfully detected:

cow.jpg → 1 cow
deer.jpg → 1 deer
elephant.jpg → 1 elephant

Prediction command:

yolo detect predict model="ml_model/weights/best.pt" source=test_images imgsz=640 conf=0.5 save=True

Prediction results are generated under:

runs/detect/predict/

The runs directory is excluded from GitHub.


---

## Backend

The backend is implemented using Flask.

Main backend components:

backend/
├── app.py
├── detector.py
├── alert.py
├── config.py
└── requirements.txt


### Backend Workflow

Image
  ↓
POST /detect
  ↓
YOLOv8 Detector
  ↓
Detection Results
  ↓
Animal
Confidence
Bounding Box
  ↓
Alert Generator
  ↓
Buzzer / LED / GSM


---

## API

### POST /detect

The backend accepts an image and performs animal detection using the trained YOLOv8 model.

Example request:

POST /detect

Content-Type: multipart/form-data


### Example Response

{
    "success": true,
    "detections": [
        {
            "animal": "elephant",
            "confidence": 0.91,
            "bounding_box": [120, 80, 420, 500]
        }
    ],
    "alerts": [
        {
            "animal": "elephant",
            "severity": "HIGH",
            "message": "Elephant detected! Take immediate action."
        }
    ]
}


---

## Hardware

The hardware integration is designed around an ESP32-CAM.

Hardware-related code is located at:

hardware/
└── esp32_cam/
    └── esp32_cam.ino


### Main Hardware Components

- ESP32-CAM
- PIR Motion Sensor
- Buzzer
- LED
- GSM Module


---

## Hardware and ML Integration

The intended end-to-end operation is:

Animal approaches agricultural field
        ↓
PIR detects movement
        ↓
ESP32-CAM captures image
        ↓
Image sent to Flask backend
        ↓
YOLOv8 detects animal
        ↓
Cow / Deer / Elephant
        ↓
Alert generated
        ↓
Buzzer
LED
GSM notification


The YOLOv8 model runs on the backend/server rather than directly on the ESP32-CAM.


---

## Technologies Used

### Machine Learning

- Python
- YOLOv8
- Ultralytics
- PyTorch
- FiftyOne
- Open Images V7
- OpenCV

### Backend

- Python
- Flask
- REST API

### Hardware

- ESP32-CAM
- PIR Motion Sensor
- Buzzer
- LED
- GSM Module

### Development Tools

- Visual Studio Code
- Git
- GitHub


---

## Installation

Clone the repository:

git clone https://github.com/sejalgajbhiye-ui/Crop-Suraksha-Kavach.git

Navigate into the project directory:

cd Crop-Suraksha-Kavach

Create a Python virtual environment:

python -m venv venv

Activate the virtual environment on Windows:

.\venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt


---

## Running the Backend

Start the Flask application:

python backend/app.py

The backend will start locally and expose the detection API.

Use:

POST /detect

to send an image for detection.


---

## Testing the Model

To test the trained model directly:

yolo detect predict model="ml_model/weights/best.pt" source=test_images imgsz=640 conf=0.5 save=True


To evaluate the model on the test set:

yolo detect val model="ml_model/weights/best.pt" data=dataset/data.yaml split=test imgsz=640 device=cpu


---

## Important Notes

- The training dataset is not included in this repository because of its size.
- The runs directory containing training outputs is excluded from GitHub.
- The trained best.pt model is included for inference.
- The ESP32-CAM is intended to capture and transmit images to the backend.
- YOLOv8 inference is performed on the backend/server.
- The current ML model detects only Cow, Deer and Elephant.


---

## Future Improvements

Possible future improvements include:

- Real-time video streaming
- Improved detection accuracy using a larger and more diverse dataset
- GPU-based inference for faster processing
- Edge deployment for reduced server dependency
- SMS integration using GSM hardware
- Mobile application for farmers
- Detection history and event logging
- Night-time detection improvements
- Additional animal classes
- Cloud/server deployment


---

## Project Contributions

The project consists of three major components.

### Machine Learning

- Dataset preparation using FiftyOne
- Dataset filtering and class mapping
- Cattle to cow class mapping
- YOLO annotation generation
- YOLOv8 model training
- Model evaluation
- Model inference

### Backend

- Flask REST API
- Image processing
- YOLO model integration
- Detection result generation
- Alert generation

### Hardware

- ESP32-CAM image capture
- Motion detection
- Buzzer and LED alerts
- GSM communication interface


---

## License

This project is developed for educational and project demonstration purposes.

See the LICENSE file for details.
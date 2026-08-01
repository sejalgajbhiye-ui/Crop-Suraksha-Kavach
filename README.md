# Crop Suraksha Kavach

## AI-Based Animal Detection and Alert System

Crop Suraksha Kavach is an AI-based agricultural safety system designed to detect animals entering agricultural fields and generate alerts to help protect farmers and crops.

The system combines a YOLOv8-based object detection model, a Flask backend, a simple web interface, and a proposed ESP32-CAM-based hardware setup.

The Machine Learning component detects three target animal classes:

- Cow
- Deer
- Elephant

The primary focus of the ML component is dataset preparation, object detection model training, evaluation, and inference.

---

## Project Objectives

The main objectives of Crop Suraksha Kavach are:

- Detect animals entering agricultural fields.
- Identify the type of animal using an object detection model.
- Provide the detected animal and confidence score.
- Generate an appropriate alert based on the detected animal.
- Provide a simple interface for monitoring detections.
- Provide a hardware architecture using ESP32-CAM for future field deployment.

---

## System Architecture

```text
ESP32-CAM / Camera
        |
        v
Image / Video Frame
        |
        v
Flask Backend
        |
        v
YOLOv8 Object Detection Model
        |
        v
Animal Detection
        |
        +------------------+
        |                  |
        v                  v
Animal Information      Alert Generation
        |
        v
Frontend Monitoring Interface
Machine Learning

The Machine Learning component is the primary technical contribution of this project.

YOLOv8 is used for object detection because it can detect both the class of an animal and its location using bounding boxes.

Target Classes
Class 0 → Cow
Class 1 → Deer
Class 2 → Elephant
Dataset

The dataset was prepared using FiftyOne and the Open Images dataset.

The required classes were selected from the dataset:

Cattle
Deer
Elephant

The original Cattle class was mapped to the project class Cow.

The final dataset contains approximately 3000 images.

Dataset Preparation Workflow
Open Images Dataset
        |
        v
FiftyOne
        |
        v
Select Cattle, Deer and Elephant
        |
        v
Cattle → Cow
        |
        v
Convert annotations to YOLO format
        |
        v
Split dataset
        |
        v
Train / Validation / Test
Dataset Split

The 3000 images were divided into three subsets:

Dataset Split	Images	Percentage
Training	2100	70%
Validation	600	20%
Testing	300	10%
Total	3000	100%

## Model Training

Command:

yolo detect train data=dataset/data.yaml model=yolov8n.pt epochs=50 imgsz=640 batch=8 device=cpu

| Parameter | Value |
|---|---|
| Model | YOLOv8n |
| Total Images | 3000 |
| Training Images | 2100 |
| Validation Images | 600 |
| Testing Images | 300 |
| Epochs | 50 |
| Image Size | 640 × 640 |
| Batch Size | 8 |
| Device | CPU |

## Model Evaluation

The trained `best.pt` model was evaluated on the separate 300-image test dataset.

| Metric    | Score |
|-----------|-------|
| Precision | 0.845 |
| Recall    | 0.671 |
| mAP@50    | 0.776 |
| mAP@50-95 | 0.526 |

### Class-wise mAP@50

| Class | mAP@50 |
|---|---:|
| Cow | 0.689 |
| Deer | 0.787 |
| Elephant | 0.853 |

The dataset follows the YOLO directory structure:

dataset/
├── train/
│   ├── images/
│   └── labels/
│
├── valid/
│   ├── images/
│   └── labels/
│
├── test/
│   ├── images/
│   └── labels/
│
└── data.yaml

The large dataset image files are not included in the GitHub repository in order to keep the repository lightweight.

Model Training

The project uses:

Model: YOLOv8n
Epochs: 50
Image Size: 640 × 640
Batch Size: 8
Device: CPU

The model was trained using the Ultralytics YOLO framework.

Training command:

yolo detect train data=dataset/data.yaml model=yolov8n.pt epochs=50 imgsz=640 batch=8 device=cpu

The trained model produces a best.pt file containing the learned weights.

Model Evaluation

After training, the model was evaluated on the separate test dataset containing 300 images.

Evaluation command:

yolo detect val model="runs/detect/train-4/weights/best.pt" data=dataset/data.yaml split=test imgsz=640 device=cpu
Overall Test Results
Metric	Result
Precision	0.845
Recall	0.671
mAP@50	0.776
mAP@50-95	0.526

These results were obtained from evaluation on the 300-image test dataset.

Class-Wise Results
mAP@50
Class	mAP@50
Cow	0.689
Deer	0.787
Elephant	0.853

The model achieved the highest mAP@50 for elephant detection and the lowest for cow detection.

Inference Testing

The trained model was also tested on individual sample images.

Example inference results:

cow.jpg
→ 1 cow detected

deer.jpg
→ 1 deer detected

elephant.jpg
→ 1 elephant detected

Inference command:

yolo detect predict model="runs/detect/train-4/weights/best.pt" source=test_images imgsz=640 conf=0.5 save=True

The resulting detection images contain the predicted animal class and bounding box.

Trained Model

The trained model is based on YOLOv8n.

The important trained model file is:

ml_model/
└── weights/
    └── best.pt

The model contains the learned weights required to perform detection of:

Cow
Deer
Elephant
Backend

The backend is implemented using Flask.

The backend acts as the bridge between the frontend and the trained ML model.

The basic processing flow is:

Image
  |
  v
Flask API
  |
  v
YOLOv8 Model
  |
  v
Prediction
  |
  +------------------+
  |                  |
  v                  v
Animal             Confidence
  |
  v
Bounding Box
  |
  v
Alert Information

The primary detection endpoint is:

POST /detect

An image can be sent to the backend, which processes it using the trained YOLOv8 model.

An example response is:

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
Frontend

The project contains a simple web-based monitoring interface.

The frontend does not require user login or signup.

The interface is designed to provide:

Start monitoring option
Camera display
Animal detection information
Confidence score
Detection status
Alert information

Frontend structure:

frontend/
├── index.html
├── script.js
└── style.css

The frontend communicates with the Flask backend for animal detection.

Hardware

The proposed hardware architecture uses an ESP32-CAM-based camera system.

The hardware is intended to capture images or video frames from the agricultural environment.

Proposed components include:

ESP32-CAM
Camera
PIR / motion detection sensor
Buzzer
LED
GSM module

The general hardware workflow is:

Animal Movement
       |
       v
Motion Detection
       |
       v
ESP32-CAM Captures Image
       |
       v
Backend / ML Model
       |
       v
Animal Detection
       |
       v
Alert

The physical hardware integration is part of the overall system design. The ML model has been developed and tested independently and is prepared for backend integration.

Alert System

The system can generate different alerts depending on the detected animal.

Example:

Elephant Detected
       |
       v
HIGH ALERT
       |
       v
Immediate Warning

Possible alert mechanisms include:

Buzzer
LED
GSM/SMS notification
Web notification

The exact alert mechanism can be extended depending on the final hardware implementation.

Project Structure

The current repository is organized as follows:

Crop-Suraksha-Kavach/
│
├── backend/
│
├── dataset/
│   └── data.yaml
│
├── docs/
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── hardware/
│
├── ml_model/
│   └── weights/
│       └── best.pt
│
├── test_images/
│   ├── cow.jpg
│   ├── deer.jpg
│   └── elephant.jpg
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── yolov8n.pt

Large dataset files and training artifacts are excluded from the repository using .gitignore.

Technologies Used
Machine Learning
Python
YOLOv8
Ultralytics
PyTorch
OpenCV
FiftyOne
Backend
Python
Flask
Flask-CORS
Frontend
HTML
CSS
JavaScript
Hardware
ESP32-CAM
Motion sensor
Buzzer
LED
GSM module
Installation
1. Clone the Repository
git clone https://github.com/sejalgajbhiye-ui/Crop-Suraksha-Kavach.git

Move into the project directory:

cd Crop-Suraksha-Kavach
2. Create a Virtual Environment
python -m venv venv
3. Activate the Virtual Environment

For Windows:

venv\Scripts\activate
4. Install Dependencies
pip install -r requirements.txt
Running the Backend

Start the Flask backend using:

python backend/app.py

The backend can then be accessed locally at:

http://127.0.0.1:5000
Running the Frontend

Open the frontend/index.html file using a local development server such as VS Code Live Server.

The frontend communicates with the Flask backend through the detection API.

ML Workflow

The complete Machine Learning workflow is:

Data Collection
       |
       v
Dataset Filtering
       |
       v
Select Cattle / Deer / Elephant
       |
       v
Cattle → Cow
       |
       v
YOLO Annotation Conversion
       |
       v
Dataset Splitting
       |
       v
Training
       |
       v
YOLOv8n Model
       |
       v
Model Evaluation
       |
       v
Inference Testing
       |
       v
best.pt
       |
       v
Backend Integration
ML Contribution

The main Machine Learning contribution to this project includes:

Collecting the required dataset
Using FiftyOne for dataset preparation
Filtering the required animal classes
Converting Cattle to Cow
Preparing YOLO-format annotations
Creating the training, validation and testing splits
Training a YOLOv8n object detection model
Evaluating the trained model
Measuring Precision, Recall and mAP
Testing the model using sample images
Preparing the trained best.pt model for backend integration
Limitations

The current project has the following limitations:

The model currently supports only three animal classes.
CPU-based training and inference are slower than GPU-based processing.
Model performance may vary under different lighting and environmental conditions.
Dense vegetation, occlusion and unusual animal poses may affect detection.
The physical hardware system requires further real-world testing.
Real-time performance depends on the available processing hardware.
Future Improvements

Possible future improvements include:

Adding more animal classes
Increasing dataset size and diversity
Improving model accuracy
Performing systematic error analysis
GPU-based training
Model optimization for edge devices
Real-time ESP32-CAM integration
SMS notifications using GSM
Mobile application integration
GPS-based animal location tracking
Cloud-based monitoring
Detection history and analytics
Field testing under different environmental conditions
Conclusion

Crop Suraksha Kavach demonstrates how computer vision and object detection can be used to assist farmers in identifying animals that may enter agricultural fields.

The developed YOLOv8n model was trained on 3000 images covering three target classes: Cow, Deer and Elephant.

The trained model achieved:

Precision: 0.845
Recall: 0.671
mAP@50: 0.776
mAP@50-95: 0.526

The model was also tested using individual animal images and successfully detected Cow, Deer and Elephant.

The trained model can be integrated with the Flask backend and the proposed ESP32-CAM-based hardware system to form a complete animal monitoring and alert solution.

License

This project is developed for educational and project demonstration purposes.

See the LICENSE file for more information.

Project
Crop Suraksha Kavach

AI-powered animal detection for safer and smarter agriculture.
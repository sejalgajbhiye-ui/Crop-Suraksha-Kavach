# 🌾 Crop Suraksha Kavach

> **AI-Powered Smart Animal Detection and Farmer Alert System using YOLO**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![YOLO](https://img.shields.io/badge/YOLO-Object%20Detection-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-black.svg)
![ESP32-CAM](https://img.shields.io/badge/ESP32--CAM-IoT-orange.svg)

---

## 📖 Project Overview

Crop Suraksha Kavach is an AI-powered smart surveillance system designed to protect agricultural fields from animal intrusion. The system uses an **ESP32-CAM** to capture images whenever movement is detected. The captured images are processed using a **YOLO (You Only Look Once)** object detection model to identify animals in real time.

Based on the detected animal, the system generates appropriate alerts for the farmer, helping prevent crop damage and improving farm safety.

---

## 🎯 Problem Statement

Crop damage caused by animals is a major challenge for farmers, especially in rural and forest-adjacent areas. Traditional monitoring methods require continuous human supervision, which is time-consuming and ineffective during nighttime.

Crop Suraksha Kavach automates field monitoring using Artificial Intelligence and IoT technologies, enabling early detection and timely alerts.

---

## 🎯 Objectives

- Detect animals entering agricultural fields in real time.
- Identify animals using a YOLO object detection model.
- Alert farmers immediately after detection.
- Reduce crop damage caused by animal intrusion.
- Develop an affordable and scalable smart farming solution.

---

## 🦌 Animals Detected

The current version of the system detects the following animals:

- 🐄 Cow
- 🦌 Deer
- 🐘 Elephant

---

## ⚙️ System Workflow

```text
ESP32-CAM
     │
     ▼
Capture Image
     │
     ▼
Send Image to Flask Server
     │
     ▼
YOLO Object Detection
     │
     ▼
Identify Animal
     │
     ├── Cow
     ├── Deer
     └── Elephant
     │
     ▼
Generate Alert
     │
     ▼
Notify Farmer
```

---

## ✨ Features

- Real-time animal detection
- YOLO-based object detection
- ESP32-CAM integration
- Automated farmer alert system
- Detection confidence score
- Detection history
- Web dashboard
- Expandable to additional animal classes

---

## 🛠️ Technology Stack

### Programming Language

- Python

### AI & Computer Vision

- YOLO
- OpenCV
- NumPy

### Backend

- Flask

### Hardware

- ESP32-CAM
- PIR Motion Sensor
- Buzzer
- GSM Module (Optional)

### Frontend

- HTML
- CSS
- JavaScript

### Version Control

- Git
- GitHub

---

## 📂 Project Structure

```text
Crop-Suraksha-Kavach/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── docs/
│
├── dataset/
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   ├── valid/
│   │   ├── images/
│   │   └── labels/
│   ├── test/
│   │   ├── images/
│   │   └── labels/
│   └── dataset.yaml
│
├── ml_model/
│   ├── train.py
│   ├── detect.py
│   ├── predict.py
│
├── backend/
│
├── frontend/
│
├── hardware/
│
├── screenshots/
│
└── images/
```

---

## 📦 Installation

Clone the repository

```bash
git clone https://github.com/sejalgajbhiye-ui/Crop-Suraksha-Kavach.git
```

Move into the project folder

```bash
cd Crop-Suraksha-Kavach
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Future Scope

- Live video streaming
- SMS alerts using GSM
- Mobile application
- Cloud database integration
- Multi-camera support
- Solar-powered deployment
- GPS-based field monitoring
- Animal counting and analytics
- Night vision enhancement

---

## 📸 Project Screenshots

Project screenshots will be added after implementation.

---

## 👩‍💻 Author

**Sejal Gajbhiye**

Bachelor of Technology (Computer Engineering)

---

## 📄 License

This project is developed for academic and educational purposes.
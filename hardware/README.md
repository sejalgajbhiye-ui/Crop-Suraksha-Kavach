# Hardware

The hardware layer is responsible for image acquisition and local alert triggering.

## Components

- ESP32-CAM
- PIR Motion Sensor
- Buzzer
- GSM Module (optional)

## Workflow

1. PIR sensor detects movement.
2. ESP32-CAM captures an image.
3. Image is sent to the Flask backend.
4. Backend sends the image to the YOLOv8 model.
5. Detected animal and confidence are returned.
6. Backend generates an alert.
7. Alert can be forwarded to the farmer through the configured notification mechanism.

## ESP32-CAM

The ESP32-CAM is responsible for image capture and communication with the backend.

The ML model is not executed directly on the ESP32-CAM.
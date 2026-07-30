#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// ==========================
// WiFi
// ==========================

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Replace with the IP address of the computer
// running Flask
const char* SERVER_URL =
    "http://192.168.1.100:5000/detect";


// ==========================
// Hardware pins
// ==========================

#define PIR_PIN 13
#define BUZZER_PIN 12
#define LED_PIN 4


// ==========================
// Setup
// ==========================

void setup() {

    Serial.begin(115200);

    pinMode(PIR_PIN, INPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);

    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(LED_PIN, LOW);

    connectWiFi();

    initCamera();
}


// ==========================
// Main loop
// ==========================

void loop() {

    int motion = digitalRead(PIR_PIN);

    if (motion == HIGH) {

        Serial.println("Motion detected!");

        delay(1000);

        sendImageToServer();

        delay(5000);
    }
}


// ==========================
// WiFi
// ==========================

void connectWiFi() {

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    Serial.print("Connecting to WiFi");

    while (WiFi.status() != WL_CONNECTED) {

        delay(500);

        Serial.print(".");
    }

    Serial.println();

    Serial.println("WiFi connected");

    Serial.print("ESP32 IP: ");
    Serial.println(WiFi.localIP());
}


// ==========================
// Camera
// ==========================

void initCamera() {

    camera_config_t config;

    // Camera pin configuration depends
    // on your exact ESP32-CAM board.

    // Configure your board-specific
    // camera pins here.

    Serial.println(
        "Camera initialization required"
    );
}


// ==========================
// Send image
// ==========================

void sendImageToServer() {

    camera_fb_t* fb = esp_camera_fb_get();

    if (!fb) {

        Serial.println(
            "Camera capture failed"
        );

        return;
    }

    HTTPClient http;

    http.begin(SERVER_URL);

    http.addHeader(
        "Content-Type",
        "image/jpeg"
    );

    int responseCode = http.POST(
        fb->buf,
        fb->len
    );

    Serial.print(
        "Server response: "
    );

    Serial.println(responseCode);

    if (responseCode > 0) {

        String response =
            http.getString();

        Serial.println(response);

        if (
            response.indexOf("cow") >= 0 ||
            response.indexOf("deer") >= 0 ||
            response.indexOf("elephant") >= 0
        ) {

            activateAlert();
        }
    }

    http.end();

    esp_camera_fb_return(fb);
}


// ==========================
// Alert
// ==========================

void activateAlert() {

    Serial.println(
        "ANIMAL DETECTED!"
    );

    digitalWrite(
        LED_PIN,
        HIGH
    );

    digitalWrite(
        BUZZER_PIN,
        HIGH
    );

    delay(3000);

    digitalWrite(
        BUZZER_PIN,
        LOW
    );

    digitalWrite(
        LED_PIN,
        LOW
    );
}
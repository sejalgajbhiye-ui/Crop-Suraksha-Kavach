#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>

// =====================================================
// Wi-Fi Configuration
// =====================================================

const char* WIFI_SSID = "YOUR_WIFI_NAME";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// IMPORTANT:
// Replace this with the IP address of the computer
// running your Flask backend.
//
// Example:
// http://192.168.1.100:5000/detect
//
const char* SERVER_URL = "http://192.168.1.100:5000/detect";


// =====================================================
// Hardware Pins
// =====================================================

// PIR sensor
#define PIR_PIN 13

// External buzzer
#define BUZZER_PIN 12

// ESP32-CAM onboard flash LED
#define LED_PIN 4


// =====================================================
// AI-THINKER ESP32-CAM Camera Pins
// =====================================================

#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5

#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22


// =====================================================
// Settings
// =====================================================

const unsigned long DETECTION_COOLDOWN = 5000;

unsigned long lastDetectionTime = 0;


// =====================================================
// Function Declarations
// =====================================================

void connectWiFi();
bool initCamera();
void captureAndSendImage();
void activateAlert();
void printWiFiStatus();


// =====================================================
// SETUP
// =====================================================

void setup() {

    Serial.begin(115200);

    delay(1000);

    Serial.println();
    Serial.println("====================================");
    Serial.println(" Crop Suraksha Kavach");
    Serial.println(" ESP32-CAM Animal Detection System");
    Serial.println("====================================");

    // ---------------------------------
    // Configure hardware pins
    // ---------------------------------

    pinMode(PIR_PIN, INPUT);

    pinMode(BUZZER_PIN, OUTPUT);

    pinMode(LED_PIN, OUTPUT);

    digitalWrite(BUZZER_PIN, LOW);

    digitalWrite(LED_PIN, LOW);


    // ---------------------------------
    // Connect Wi-Fi
    // ---------------------------------

    connectWiFi();


    // ---------------------------------
    // Initialize camera
    // ---------------------------------

    if (!initCamera()) {

        Serial.println("Camera initialization failed!");

        while (true) {

            digitalWrite(LED_PIN, HIGH);

            delay(200);

            digitalWrite(LED_PIN, LOW);

            delay(200);
        }
    }


    Serial.println();
    Serial.println("System ready.");
    Serial.println("Waiting for motion...");
    Serial.println();

}


// =====================================================
// MAIN LOOP
// =====================================================

void loop() {

    // Make sure Wi-Fi is connected
    if (WiFi.status() != WL_CONNECTED) {

        Serial.println("Wi-Fi disconnected.");

        connectWiFi();
    }


    // Read PIR sensor
    int motion = digitalRead(PIR_PIN);


    if (motion == HIGH) {

        unsigned long currentTime = millis();


        // Prevent repeated detections
        if (
            currentTime - lastDetectionTime
            >= DETECTION_COOLDOWN
        ) {

            Serial.println();
            Serial.println("------------------------------------");
            Serial.println("Motion detected!");
            Serial.println("Capturing image...");
            Serial.println("------------------------------------");


            captureAndSendImage();


            lastDetectionTime = currentTime;
        }
    }


    delay(100);
}


// =====================================================
// WIFI CONNECTION
// =====================================================

void connectWiFi() {

    if (WiFi.status() == WL_CONNECTED) {

        return;
    }


    Serial.print("Connecting to Wi-Fi");

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );


    int attempts = 0;


    while (
        WiFi.status() != WL_CONNECTED &&
        attempts < 30
    ) {

        delay(500);

        Serial.print(".");

        attempts++;
    }


    Serial.println();


    if (WiFi.status() == WL_CONNECTED) {

        Serial.println("Wi-Fi connected!");

        printWiFiStatus();

    } else {

        Serial.println("Wi-Fi connection failed.");
    }
}


// =====================================================
// PRINT WIFI STATUS
// =====================================================

void printWiFiStatus() {

    Serial.print("ESP32 IP Address: ");

    Serial.println(
        WiFi.localIP()
    );


    Serial.print("Backend URL: ");

    Serial.println(
        SERVER_URL
    );
}


// =====================================================
// CAMERA INITIALIZATION
// =====================================================

bool initCamera() {

    camera_config_t config;


    // ---------------------------------
    // Camera pins
    // ---------------------------------

    config.ledc_channel =
        LEDC_CHANNEL_0;

    config.ledc_timer =
        LEDC_TIMER_0;


    config.pin_d0 =
        Y2_GPIO_NUM;

    config.pin_d1 =
        Y3_GPIO_NUM;

    config.pin_d2 =
        Y4_GPIO_NUM;

    config.pin_d3 =
        Y5_GPIO_NUM;

    config.pin_d4 =
        Y6_GPIO_NUM;

    config.pin_d5 =
        Y7_GPIO_NUM;

    config.pin_d6 =
        Y8_GPIO_NUM;

    config.pin_d7 =
        Y9_GPIO_NUM;


    config.pin_xclk =
        XCLK_GPIO_NUM;

    config.pin_pclk =
        PCLK_GPIO_NUM;

    config.pin_vsync =
        VSYNC_GPIO_NUM;

    config.pin_href =
        HREF_GPIO_NUM;

    config.pin_sccb_sda =
        SIOD_GPIO_NUM;

    config.pin_sccb_scl =
        SIOC_GPIO_NUM;

    config.pin_pwdn =
        PWDN_GPIO_NUM;

    config.pin_reset =
        RESET_GPIO_NUM;


    config.xclk_freq_hz =
        20000000;


    config.pixel_format =
        PIXFORMAT_JPEG;


    // ---------------------------------
    // Camera resolution
    // ---------------------------------

    if (psramFound()) {

        config.frame_size =
            FRAMESIZE_VGA;

        config.jpeg_quality =
            10;

        config.fb_count =
            2;

    } else {

        config.frame_size =
            FRAMESIZE_QVGA;

        config.jpeg_quality =
            12;

        config.fb_count =
            1;
    }


    // ---------------------------------
    // Initialize camera
    // ---------------------------------

    esp_err_t result =
        esp_camera_init(&config);


    if (result != ESP_OK) {

        Serial.print(
            "Camera init failed. Error: 0x"
        );

        Serial.println(
            result,
            HEX
        );

        return false;
    }


    // ---------------------------------
    // Camera sensor settings
    // ---------------------------------

    sensor_t* sensor =
        esp_camera_sensor_get();


    if (sensor != nullptr) {

        sensor->set_framesize(
            sensor,
            FRAMESIZE_VGA
        );

        sensor->set_quality(
            sensor,
            10
        );
    }


    Serial.println(
        "Camera initialized successfully."
    );


    return true;
}


// =====================================================
// CAPTURE IMAGE AND SEND TO FLASK
// =====================================================

void captureAndSendImage() {

    if (
        WiFi.status() != WL_CONNECTED
    ) {

        Serial.println(
            "Wi-Fi unavailable."
        );

        return;
    }


    // ---------------------------------
    // Capture image
    // ---------------------------------

    camera_fb_t* fb =
        esp_camera_fb_get();


    if (!fb) {

        Serial.println(
            "Camera capture failed!"
        );

        return;
    }


    Serial.print(
        "Image captured. Size: "
    );

    Serial.print(
        fb->len
    );

    Serial.println(
        " bytes"
    );


    // ---------------------------------
    // Create HTTP request
    // ---------------------------------

    HTTPClient http;


    http.begin(
        SERVER_URL
    );


    // ---------------------------------
    // Multipart boundary
    // ---------------------------------

    String boundary =
        "----ESP32CameraBoundary";


    String header =
        "--" + boundary + "\r\n"
        "Content-Disposition: form-data; "
        "name=\"image\"; "
        "filename=\"camera.jpg\"\r\n"
        "Content-Type: image/jpeg\r\n\r\n";


    String footer =
        "\r\n--" +
        boundary +
        "--\r\n";


    // ---------------------------------
    // Build complete request body
    // ---------------------------------

    size_t totalLength =
        header.length()
        + fb->len
        + footer.length();


    uint8_t* requestBody =
        (uint8_t*) malloc(
            totalLength
        );


    if (!requestBody) {

        Serial.println(
            "Failed to allocate memory."
        );

        esp_camera_fb_return(fb);

        http.end();

        return;
    }


    // Copy multipart header

    memcpy(
        requestBody,
        header.c_str(),
        header.length()
    );


    // Copy JPEG

    memcpy(
        requestBody + header.length(),
        fb->buf,
        fb->len
    );


    // Copy multipart footer

    memcpy(
        requestBody +
        header.length() +
        fb->len,

        footer.c_str(),

        footer.length()
    );


    // ---------------------------------
    // Set HTTP headers
    // ---------------------------------

    String contentType =
        "multipart/form-data; boundary="
        + boundary;


    http.addHeader(
        "Content-Type",
        contentType
    );


    http.setTimeout(
        15000
    );


    Serial.println(
        "Sending image to backend..."
    );


    // ---------------------------------
    // POST request
    // ---------------------------------

    int responseCode =
        http.POST(
            requestBody,
            totalLength
        );


    // ---------------------------------
    // Process response
    // ---------------------------------

    Serial.print(
        "HTTP Response Code: "
    );

    Serial.println(
        responseCode
    );


    if (responseCode > 0) {

        String response =
            http.getString();


        Serial.println(
            "Backend response:"
        );

        Serial.println(
            response
        );


        // ---------------------------------
        // Check for detected animal
        // ---------------------------------

        if (
            response.indexOf(
                "\"success\":true"
            ) >= 0
        ) {

            if (
                response.indexOf(
                    "\"animal\":\"cow\""
                ) >= 0
                ||
                response.indexOf(
                    "\"animal\":\"deer\""
                ) >= 0
                ||
                response.indexOf(
                    "\"animal\":\"elephant\""
                ) >= 0
            ) {

                Serial.println();
                Serial.println(
                    "!!! ANIMAL DETECTED !!!"
                );

                activateAlert();
            }

        } else {

            Serial.println(
                "No animal detected."
            );
        }

    } else {

        Serial.print(
            "HTTP request failed: "
        );

        Serial.println(
            http.errorToString(
                responseCode
            )
        );
    }


    // ---------------------------------
    // Cleanup
    // ---------------------------------

    free(
        requestBody
    );


    http.end();


    esp_camera_fb_return(
        fb
    );
}


// =====================================================
// ALERT
// =====================================================

void activateAlert() {

    Serial.println();
    Serial.println(
        "===================================="
    );

    Serial.println(
        "       ANIMAL DETECTED!"
    );

    Serial.println(
        "Activating alert..."
    );

    Serial.println(
        "===================================="
    );


    // Turn ON LED

    digitalWrite(
        LED_PIN,
        HIGH
    );


    // Turn ON buzzer

    digitalWrite(
        BUZZER_PIN,
        HIGH
    );


    // Alert duration

    delay(3000);


    // Turn OFF buzzer

    digitalWrite(
        BUZZER_PIN,
        LOW
    );


    // Turn OFF LED

    digitalWrite(
        LED_PIN,
        LOW
    );


    Serial.println(
        "Alert stopped."
    );
}
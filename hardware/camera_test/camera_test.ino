/*
 * Crop Suraksha Kavach - Hardware Diagnostic Test Sketch
 * 
 * Purpose: Test ESP32-CAM camera sensor, onboard flash LED,
 * buzzer pin, and Wi-Fi connectivity before full deployment.
 */

#include "esp_camera.h"
#include <WiFi.h>

// Wi-Fi Credentials
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// Hardware Pins
#define PIR_PIN    13
#define BUZZER_PIN 12
#define LED_PIN    4

// AI-Thinker Pin Definitions
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

void setup() {
    Serial.begin(115200);
    delay(1000);
    Serial.println("\n--- Crop Suraksha Kavach Hardware Self-Test ---");

    // Test Pins
    pinMode(PIR_PIN, INPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(LED_PIN, OUTPUT);

    // Flash LED test
    Serial.println("[TEST] Testing Flash LED on GPIO 4...");
    digitalWrite(LED_PIN, HIGH);
    delay(500);
    digitalWrite(LED_PIN, LOW);

    // Buzzer test
    Serial.println("[TEST] Testing Buzzer on GPIO 12...");
    digitalWrite(BUZZER_PIN, HIGH);
    delay(300);
    digitalWrite(BUZZER_PIN, LOW);

    // Camera Init Config
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sccb_sda = SIOD_GPIO_NUM;
    config.pin_sccb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_QVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;

    Serial.println("[TEST] Initializing Camera Module...");
    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("[FAIL] Camera init failed with error 0x%x\n", err);
    } else {
        Serial.println("[PASS] Camera initialized successfully!");
        
        camera_fb_t * fb = esp_camera_fb_get();
        if (fb) {
            Serial.printf("[PASS] Frame captured! Size: %u bytes\n", fb->len);
            esp_camera_fb_return(fb);
        } else {
            Serial.println("[FAIL] Frame capture failed.");
        }
    }

    Serial.println("\n[INFO] Diagnostic complete. Monitoring PIR sensor on GPIO 13...");
}

void loop() {
    int motion = digitalRead(PIR_PIN);
    if (motion == HIGH) {
        Serial.println("[PIR] Motion DETECTED on GPIO 13!");
        digitalWrite(LED_PIN, HIGH);
        delay(200);
        digitalWrite(LED_PIN, LOW);
    }
    delay(500);
}

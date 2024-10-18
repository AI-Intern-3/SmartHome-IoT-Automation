#include <WiFi.h>
#include <PubSubClient.h>
#include <FS.h>
#include <SPI.h>
#include <SD.h>
#include <Wire.h>

const char* ssid = "your_wifi_ssid"; // Your Wi-Fi SSID
const char* password = "your_wifi_password"; // Your Wi-Fi password
const char* aws_endpoint = "your_aws_endpoint.iot.us-west-2.amazonaws.com"; // Your AWS IoT endpoint
const char* sensorTopic = "esp32/sensordata"; // Your sensor data topic
const char* controlTopic = "home/automation/control"; // Control topic

// Certificates
const char* aws_cert = "-----BEGIN CERTIFICATE-----\nYOUR_CERTIFICATE_CONTENT\n-----END CERTIFICATE-----\n";
const char* aws_private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_CONTENT\n-----END PRIVATE KEY-----\n";
const char* aws_root_ca = "-----BEGIN CERTIFICATE-----\nYOUR_ROOT_CA_CONTENT\n-----END CERTIFICATE-----\n";

// Relay pin definitions
const int relay1Pin = 23;
const int relay2Pin = 22;
const int relay3Pin = 21;
const int relay4Pin = 19;

WiFiClientSecure net;
PubSubClient client(net);

void setup() {
    Serial.begin(115200);

    // Set relay pins as output
    pinMode(relay1Pin, OUTPUT);
    pinMode(relay2Pin, OUTPUT);
    pinMode(relay3Pin, OUTPUT);
    pinMode(relay4Pin, OUTPUT);
    
    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi!");

    // Configure secure connection
    net.setCACert(aws_root_ca);
    net.setCertificate(aws_cert);
    net.setPrivateKey(aws_private_key);
    
    // Set MQTT server
    client.setServer(aws_endpoint, 8883);
    client.setCallback(mqttCallback);

    // Connect to AWS IoT Core
    connectToAWS();
}

void loop() {
    if (!client.connected()) {
        connectToAWS();
    }
    client.loop();
  
    // Example sensor data (Replace with actual sensor reading)
    float temperature = analogRead(34);  // Replace with actual sensor reading
    float humidity = analogRead(35);
    float gas = analogRead(36);
    
    // Prepare data to send
    char payload[512];
    snprintf(payload, sizeof(payload), "{\"temperature\": %.2f, \"humidity\": %.2f, \"gas\": %.2f}", temperature, humidity, gas);
    
    // Publish data to AWS IoT
    if (client.publish(sensorTopic, payload)) {
        Serial.println("Data published: " + String(payload));
    } else {
        Serial.println("Data publishing failed.");
    }

    delay(5000); // Adjust the delay as necessary
}

void connectToAWS() {
    while (!client.connected()) {
        Serial.print("Connecting to AWS IoT...");
        if (client.connect("ESP32Client")) {
            Serial.println("connected!");
            // Subscribe to control topic
            client.subscribe(controlTopic);
        } else {
            Serial.print("failed with state ");
            Serial.println(client.state());
            delay(2000);
        }
    }
}

void mqttCallback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Message arrived [");
    Serial.print(topic);
    Serial.print("]: ");
    
    String message;
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    Serial.println(message);

    // Control relays based on the message received
    controlRelays(message);
}

void controlRelays(String message) {
    if (message == "RELAY1_ON") {
        digitalWrite(relay1Pin, HIGH);
        Serial.println("Relay 1 is ON");
    } else if (message == "RELAY1_OFF") {
        digitalWrite(relay1Pin, LOW);
        Serial.println("Relay 1 is OFF");
    } else if (message == "RELAY2_ON") {
        digitalWrite(relay2Pin, HIGH);
        Serial.println("Relay 2 is ON");
    } else if (message == "RELAY2_OFF") {
        digitalWrite(relay2Pin, LOW);
        Serial.println("Relay 2 is OFF");
    } else if (message == "RELAY3_ON") {
        digitalWrite(relay3Pin, HIGH);
        Serial.println("Relay 3 is ON");
    } else if (message == "RELAY3_OFF") {
        digitalWrite(relay3Pin, LOW);
        Serial.println("Relay 3 is OFF");
    } else if (message == "RELAY4_ON") {
        digitalWrite(relay4Pin, HIGH);
        Serial.println("Relay 4 is ON");
    } else if (message == "RELAY4_OFF") {
        digitalWrite(relay4Pin, LOW);
        Serial.println("Relay 4 is OFF");
    }
}

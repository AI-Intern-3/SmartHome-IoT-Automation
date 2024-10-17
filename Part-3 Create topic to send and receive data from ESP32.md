# Communication from ESP32 to AWS IoT Core

Here’s a detailed guide on how to program the ESP32 for communication with AWS IoT Core, along with steps to test the communication.

## Step 1: Set Up the Arduino IDE

1. **Install Arduino IDE**: If you haven't already, download and install the Arduino IDE from the [official Arduino website](https://www.arduino.cc/en/software).

2. **Install the ESP32 Board in Arduino IDE**:
   - Open Arduino IDE.
   - Go to **File** > **Preferences**.
   - In the "Additional Boards Manager URLs" field, add the following URL:
     ```
     https://dl.espressif.com/dl/package_esp32_index.json
     ```
   - Click **OK**.
   - Go to **Tools** > **Board** > **Boards Manager**.
   - Search for "ESP32" and install the latest version of the ESP32 board package.

3. **Install Required Libraries**:
   - Go to **Sketch** > **Include Library** > **Manage Libraries**.
   - Search for and install the following libraries:
     - `WiFi`
     - `PubSubClient` (for MQTT communication)
     - `ArduinoJson` (optional, for JSON data formatting)

## Step 2: Code for ESP32

Here's a sample code to establish communication between the ESP32 and AWS IoT Core:

```cpp
#include <WiFi.h>
#include <PubSubClient.h>

// AWS IoT Core settings
const char* ssid = "YOUR_SSID"; // Your Wi-Fi SSID
const char* password = "YOUR_PASSWORD"; // Your Wi-Fi password
const char* aws_endpoint = "YOUR_AWS_IOT_ENDPOINT"; // Your AWS IoT endpoint (without https:// and trailing /)
const char* aws_cert = "-----BEGIN CERTIFICATE-----\nYOUR_CERTIFICATE_CONTENT\n-----END CERTIFICATE-----\n";
const char* aws_private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_CONTENT\n-----END PRIVATE KEY-----\n";
const char* aws_root_ca = "-----BEGIN CERTIFICATE-----\nYOUR_ROOT_CA_CONTENT\n-----END CERTIFICATE-----\n";

// MQTT topics
const char* sensorTopic = "home/automation/sensors";
const char* controlTopic = "home/automation/control";

WiFiClientSecure net;
PubSubClient client(net);

void setup() {
  Serial.begin(115200);
  
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
  
  // Publish sensor data (example)
  String sensorData = "{\"temperature\": 24.5, \"humidity\": 60}";
  client.publish(sensorTopic, sensorData.c_str());
  Serial.println("Published data: " + sensorData);
  
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
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}



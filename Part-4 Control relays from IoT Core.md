

# Controlling Devices via Relays with AWS IoT Core and ESP32

Great to hear that you've established communication between AWS IoT Core and your ESP32! Now, to control devices connected to relays via your ESP32, you can follow these steps:

## Step 1: Set Up the Hardware

### 1. Connect the Relays

Connect the relay module to the ESP32 GPIO pins. For example:
- Relay 1: GPIO 23
- Relay 2: GPIO 22
- Relay 3: GPIO 21
- Relay 4: GPIO 19

### 2. Power Supply
Ensure the relay module has the appropriate power supply, as they often require more current than the ESP32 can provide directly.

### 3. Wiring
Connect the common (COM) terminal of the relay to your device’s power source.
- Connect the Normally Open (NO) terminal to the device you want to control.
- Connect the relay control pins to the respective GPIO pins on the ESP32.

## Step 2: Update the ESP32 Code

You need to modify your existing ESP32 code to control the relays based on messages received from AWS IoT Core. Below is an updated example code snippet:

```cpp
#include <WiFi.h>
#include <PubSubClient.h>

// AWS IoT Core settings
const char* ssid = "YOUR_SSID"; // Your Wi-Fi SSID
const char* password = "YOUR_PASSWORD"; // Your Wi-Fi password
const char* aws_endpoint = "YOUR_AWS_IOT_ENDPOINT"; // Your AWS IoT endpoint
const char* aws_cert = "-----BEGIN CERTIFICATE-----\nYOUR_CERTIFICATE_CONTENT\n-----END CERTIFICATE-----\n";
const char* aws_private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_CONTENT\n-----END PRIVATE KEY-----\n";
const char* aws_root_ca = "-----BEGIN CERTIFICATE-----\nYOUR_ROOT_CA_CONTENT\n-----END CERTIFICATE-----\n";

// MQTT topics
const char* sensorTopic = "home/automation/sensors";
const char* controlTopic = "home/automation/control";

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
  
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  // Control relays based on the message received
  if (topic == controlTopic) {
    controlRelays(message);
  }
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
```

# Step 3: Publish Control Messages from AWS IoT Core

To control the relays, you can send commands to the home/automation/control topic from the AWS IoT Core console or via an application.

Example Control Messages

To turn Relay 1 ON: RELAY1_ON

To turn Relay 1 OFF: RELAY1_OFF

To turn Relay 2 ON: RELAY2_ON

To turn Relay 2 OFF: RELAY2_OFF

To turn Relay 3 ON: RELAY3_ON

To turn Relay 3 OFF: RELAY3_OFF

To turn Relay 4 ON: RELAY4_ON

To turn Relay 4 OFF: RELAY4_OFF


# Step 4: Testing the Control Functionality

1. Upload the Updated Code: Make sure to upload the updated ESP32 code with relay control functionality.


2. Monitor Serial Output: Open the Serial Monitor in Arduino IDE (Ctrl + Shift + M) to observe the ESP32's connection status and relay control messages.


3. Send Commands from AWS IoT Core: Go to the AWS IoT Core console, navigate to Test > MQTT test client.

Subscribe to the home/automation/control topic.

Publish relay control commands (e.g., RELAY1_ON).



4. Observe the Changes: You should see the corresponding relay turning ON or OFF as per the command sent, along with the serial output indicating the relay's.

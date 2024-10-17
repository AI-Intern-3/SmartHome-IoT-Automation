To read, store, and manage data from sensors connected to an ESP32 and store it in an AWS database, we will use AWS IoT Core to handle communication between the ESP32 and AWS services, and AWS DynamoDB as the database to store the sensor data. Below are the detailed steps to achieve this:


---

Step 1: Connect Sensors to ESP32

1. Hardware Setup:

Ensure that your sensors are connected properly to the ESP32's GPIO pins. For example:

DHT11 (temperature/humidity) sensor connected to GPIO 15.

MQ-2 (gas) sensor connected to GPIO 35 (analog).

LDR (light) sensor connected to GPIO 34 (analog).

Any additional sensors connected accordingly.




2. Install Required Libraries:

Install libraries in the Arduino IDE or PlatformIO to support sensor reading:

DHT.h for DHT sensors.

WiFi.h for Wi-Fi connection.

PubSubClient.h for MQTT communication with AWS IoT Core.






---

Step 2: Set Up AWS IoT Core

1. Create an IoT Thing in AWS:

Go to the AWS IoT Console → Manage → Things → Create Thing.

Create a new Thing (e.g., ESP32_Sensors).

Download and save the device certificate, private key, and root CA certificate.



2. Attach Policy to IoT Thing:

Create a new IoT policy to allow the ESP32 to publish sensor data to AWS IoT Core.

Go to Secure → Policies → Create policy.

Use the following permissions for the policy:

iot:Publish, iot:Subscribe, iot:Connect

Resource: arn:aws:iot:your-region:your-account-id:topic/esp32/sensors

Effect: Allow


Attach this policy to the certificate of your ESP32 Thing.





---

Step 3: Write ESP32 Code to Send Data to AWS IoT Core

1. Connect ESP32 to Wi-Fi:

Use the WiFi.h library to connect the ESP32 to a Wi-Fi network.



2. Read Sensor Data:

Write code to read sensor values from the connected sensors (DHT11, LDR, MQ-2, etc.).



3. Send Sensor Data to AWS IoT Core:

Use MQTT to publish the sensor data to AWS IoT Core.


Example code to send data from the ESP32:

#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// Pin definitions for sensors
#define DHTPIN 15  // DHT11 sensor pin
#define DHTTYPE DHT11
#define LDR_PIN 34 // LDR pin
#define GAS_PIN 35 // MQ-2 pin

// Wi-Fi credentials
const char* ssid = "your_wifi_ssid";
const char* password = "your_wifi_password";

// AWS IoT Core credentials
const char* mqtt_server = "your-aws-iot-endpoint";

WiFiClientSecure espClient;
PubSubClient client(espClient);

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Connect to AWS IoT Core
  espClient.setCACert(AWS_ROOT_CA);
  espClient.setCertificate(AWS_CERTIFICATE);
  espClient.setPrivateKey(AWS_PRIVATE_KEY);
  client.setServer(mqtt_server, 8883);
}

void loop() {
  // Reconnect if not connected
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Read sensor data
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  int ldrValue = analogRead(LDR_PIN);
  int gasValue = analogRead(GAS_PIN);

  // Prepare JSON payload to send
  String payload = "{";
  payload += "\"temperature\": " + String(temperature, 2) + ",";
  payload += "\"humidity\": " + String(humidity, 2) + ",";
  payload += "\"light\": " + String(ldrValue) + ",";
  payload += "\"gas\": " + String(gasValue);
  payload += "}";

  Serial.print("Sending payload: ");
  Serial.println(payload);

  // Publish data to AWS IoT Core
  client.publish("esp32/sensors", payload.c_str());

  // Wait for 10 seconds
  delay(10000);
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("Connected to AWS IoT");
      client.subscribe("esp32/sensors");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      delay(5000);
    }
  }
}




---

Step 4: Create DynamoDB Table to Store Sensor Data

1. Create DynamoDB Table:

Go to AWS DynamoDB Console → Tables → Create Table.

Table Name: SensorData.

Primary Key:

sensorId (String) – to uniquely identify the sensor.

timestamp (String) – to store the timestamp of the data.




2. Configure AWS IoT Rule to Insert Data into DynamoDB:

Go to AWS IoT Core → Act → Rules → Create Rule.

Enter a SQL query for the rule:

SELECT * FROM 'esp32/sensors'

Add a DynamoDB action:

Choose the SensorData table.

Map the incoming JSON attributes (e.g., temperature, humidity, light, and gas) to DynamoDB table columns.

Map the sensorId and timestamp fields accordingly.






---

Step 5: Process and Store Data in AWS DynamoDB

1. AWS Lambda (Optional):

If additional processing is required, you can trigger an AWS Lambda function from the IoT Rule to process the data before saving it in DynamoDB.


Example Lambda function to insert processed data into DynamoDB:

import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SensorData')

def lambda_handler(event, context):
    sensor_data = json.loads(event['data'])

    table.put_item(
        Item={
            'sensorId': event['sensorId'],
            'timestamp': str(datetime.now()),
            'temperature': sensor_data['temperature'],
            'humidity': sensor_data['humidity'],
            'light': sensor_data['light'],
            'gas': sensor_data['gas']
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Data stored successfully!')
    }




---

Step 6: Verify the Setup

1. Run the ESP32 Program:

Flash the ESP32 with the code written in Step 3.

The ESP32 will start reading data from the sensors and publishing it to AWS IoT Core.



2. Check Data in DynamoDB:

Go to AWS DynamoDB → Tables → SensorData.

Verify that the data from the ESP32 sensors is being saved in the table with correct timestamp and sensor values.





---

Summary

ESP32 reads data from sensors like DHT11, MQ-2, and LDR.

ESP32 connects to AWS IoT Core over MQTT to publish sensor data to a topic (esp32/sensors).

AWS IoT Core is configured to route the data to DynamoDB via an IoT rule.

Data is stored in a DynamoDB table (SensorData) with appropriate fields.

The system can be expanded to trigger AWS Lambda for further data processing if needed.


This approach allows you to efficiently store real-time sensor data from ESP32 into an AWS-managed database for further analysis or monitoring.


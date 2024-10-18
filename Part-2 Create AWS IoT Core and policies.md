# Connecting ESP32 to Amazon AWS IoT Core using MQTT

## Overview
This is a beginner tutorial on connecting the **ESP32** to **AWS IoT Core** using MQTT for IoT applications. We'll use a **DHT11** sensor to collect humidity and temperature data and publish it to the AWS MQTT server. The key steps include:

- Signing up for and configuring AWS IoT Core.
- Installing necessary Arduino libraries.
- Creating a Thing in AWS IoT Core.
- Generating and attaching policies and certificates.
- Writing and modifying the Arduino sketch to connect ESP32 to AWS IoT Core.
- Publishing and subscribing to sensor data on AWS.

## Hardware Setup
- **ESP32** WiFi module
- **DHT11** Humidity and Temperature sensor

Follow the circuit diagram to connect the **DHT11 sensor** to the **ESP32** board. You can use a breadboard or male-to-female connector wires.

## What is Amazon AWS IoT Core?
AWS IoT Core is a managed cloud service that allows you to securely connect IoT devices to cloud applications. It supports the following protocols:
- **MQTT**
- **MQTT over WSS**
- **HTTPS**
- **LoRaWAN**

## Steps for Connecting ESP32 to AWS IoT Core

### 1. **Signing Up for AWS IoT Core**
- Go to [aws.amazon.com/iot-core](https://aws.amazon.com/iot-core/).
- Create an AWS account using an email address and password. You’ll need to provide credit card and phone number details for verification.

### 2. **AWS IoT Core Dashboard**
- After signing in, open the **AWS Management Console**.
- Search for **IoT Core** and open the **AWS IoT Dashboard**.
- On the left panel, you will find the **Manage** and **Secure** options, which are key for creating Things and managing security policies.

### 3. **Creating a Thing**
To create a Thing in AWS IoT:
- Navigate to the **Manage** section.
- Click on **Create Things**.
- Select **Create a single thing** and click **Next**.
- Name your thing (e.g., `ESP32_DHT11`), and set **No shadow** for device shadow configuration.
- Click **Next** to proceed.

### 4. **Generating Device Certificate**
- Select **Auto Generate New Certificate** for simplicity.
- Click **Next** to move forward.

### 5. **Creating and Attaching a Policy**
- Create a new policy by navigating to the **Secure** section.
- Give the policy a name, e.g., `ESP32_Policy`.
- Add a statement allowing the actions: `iot:Publish`, `iot:Subscribe`, `iot:Connect`, and `iot:Receive`.
- Attach this policy to the Thing's certificate.

### 6. **Downloading Certificates and Keys**
Download the following:
- **Device certificate** (rename it for easier identification).
- **Public key** and **Private key** (rename them for clarity).
- **Root CA1** certificate.

### 7. **Installing Necessary Arduino Libraries**
To communicate with AWS IoT using ESP32, install the following libraries in the **Arduino IDE**:
1. **ArduinoJSON Library**:
   - Go to **Library Manager**, search for `JSON`, and install.
2. **PubSubClient Library**:
   - Search for `PubSubClient` by Nick O’Leary and install.
3. **DHT11 Sensor Library**:
   - Search for `dht11` and install.

### 8. **Modifying the Arduino Sketch**
In the sketch:
- Include the necessary libraries.
- Modify the WiFi credentials and AWS IoT credentials, including the Thing’s name, certificate, and key details.

### 9. **Publish and Subscribe to AWS IoT**
After uploading the sketch to the ESP32:
- Use the AWS IoT Core dashboard to monitor messages published by the ESP32.
- Subscribe to receive data sent from the ESP32 to AWS.

## Conclusion
By following these steps, you will be able to connect the ESP32 to AWS IoT Core and use MQTT to publish sensor data to the cloud. AWS IoT Core provides a powerful and scalable solution for IoT applications.


Selected Hardware Components

1. ESP32 Development Board:

Description: The ESP32 is a powerful microcontroller with built-in Wi-Fi and Bluetooth capabilities, making it ideal for IoT applications.

Recommended Model:

ESP32 DevKit v1

Features:

Dual-core processor

Integrated Wi-Fi (802.11 b/g/n)

Bluetooth (Classic and BLE)

Multiple GPIO pins

Support for various peripherals (I2C, SPI, UART, etc.)

Suitable for development with Arduino IDE or PlatformIO





2. 4-Channel Relay Module:

Description: A relay module allows you to control high-voltage appliances using low-voltage signals from the ESP32.

Recommended Model:

5V 4-Channel Relay Module

Features:

4 independent relays for controlling multiple devices

Opto-isolated inputs for safety

Can control AC devices up to 250V/10A or DC devices

LED indicators for relay status

Easy connection with ESP32 via GPIO pins





3. Power Supply:

Description: A reliable power source is essential to power the ESP32 and the relay module.

Recommended Model:

USB Power Adapter or 5V Power Supply

Features:

USB power adapters (like those for smartphones) can directly power the ESP32 via the micro-USB port.

Alternatively, use a 5V DC power supply connected to the relay module.





4. Additional Components:

Breadboard and Jumper Wires:

For prototyping and connecting components without soldering.


Power Switch (optional):

To easily turn on/off the entire setup.





Wiring Diagram

Here’s a simple wiring guide for connecting the ESP32 to the 4-channel relay module:

1. ESP32 to Relay Module Connections:

Relay IN1: Connect to GPIO 23 (or any other GPIO pin).

Relay IN2: Connect to GPIO 22.

Relay IN3: Connect to GPIO 21.

Relay IN4: Connect to GPIO 19.

VCC: Connect to the 5V pin of the relay module (can also be powered via the USB if using the USB power adapter).

GND: Connect to the GND pin of the ESP32.



2. Relay Connections:

Connect the appliances you want to control to the relay terminals as follows:

NO (Normally Open): Connect to the live wire of the appliance.

COM (Common): Connect to the power source (AC or DC).





Summary

With the ESP32 Development Board and 4-Channel Relay Module, you will have a robust setup for controlling multiple devices wirelessly via AWS IoT Core. The ESP32’s capabilities allow you to expand your project easily with additional sensors, actuators, and functionalities in the future.

If you need any help with purchasing options or specific configurations, let me know!



Selected Sensors

1. DHT22 (Temperature and Humidity Sensor)

Connection Type: Digital

Wi-Fi Capability: Not applicable (data will be sent via ESP32)

Features: Measures temperature and humidity; connects to the ESP32 GPIO pin to send data.



2. HC-SR501 (PIR Motion Sensor)

Connection Type: Digital

Wi-Fi Capability: Not applicable (data will be sent via ESP32)

Features: Detects motion; connects to the ESP32 GPIO pin to trigger actions or send notifications.



3. MQ-2 (Gas Sensor)

Connection Type: Analog

Wi-Fi Capability: Not applicable (data will be sent via ESP32)

Features: Detects gases like LPG and smoke; connects to an analog pin on the ESP32.



4. ESP32-CAM (Camera Module)

Connection Type: Digital

Wi-Fi Capability: Yes

Features: Captures images and streams video; connects to the ESP32 via GPIO and can send data over Wi-Fi.




Integration with ESP32

Wiring Connections

1. DHT22 Sensor:

VCC: Connect to 3.3V on ESP32.

GND: Connect to GND on ESP32.

DATA: Connect to a digital GPIO pin (e.g., GPIO 23).



2. HC-SR501 PIR Motion Sensor:

VCC: Connect to 5V on ESP32.

GND: Connect to GND on ESP32.

OUT: Connect to a digital GPIO pin (e.g., GPIO 22).



3. MQ-2 Gas Sensor:

VCC: Connect to 5V on ESP32.

GND: Connect to GND on ESP32.

A0: Connect to an analog GPIO pin (e.g., GPIO 34).



4. ESP32-CAM:

Connect according to its pinout, ensuring it has power from the ESP32. The camera module can be powered by 5V from the ESP32.

For sending images or video, utilize the ESP32's Wi-Fi capabilities to stream or send data.





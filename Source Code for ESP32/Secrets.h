// Secrets.h

#ifndef SECRETS_H
#define SECRETS_H

// Wi-Fi Credentials
const char* WIFI_SSID = "your_wifi_ssid";
const char* WIFI_PASSWORD = "your_wifi_password";

// AWS IoT Credentials
const char* AWS_ENDPOINT = "your_aws_endpoint.iot.us-west-2.amazonaws.com";
const char* AWS_CERT = "-----BEGIN CERTIFICATE-----\nYOUR_CERTIFICATE_CONTENT\n-----END CERTIFICATE-----\n";
const char* AWS_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_CONTENT\n-----END PRIVATE KEY-----\n";
const char* AWS_ROOT_CA = "-----BEGIN CERTIFICATE-----\nYOUR_ROOT_CA_CONTENT\n-----END CERTIFICATE-----\n";

// MQTT Topics
const char* SENSOR_TOPIC = "esp32/sensordata";
const char* CONTROL_TOPIC = "home/automation/control";

#endif // SECRETS_H

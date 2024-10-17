To create a DynamoDB database and table for storing data from sensors connected to your ESP32 module, follow these detailed steps. DynamoDB is a fully managed NoSQL database offered by AWS, which is suitable for storing sensor data in real time.

## Step 1: Create a DynamoDB Table

1. Login to AWS Management Console:

Go to AWS Console.

In the search bar, type DynamoDB and select DynamoDB.



2. Create a New Table:

In the DynamoDB console, click on Create table.



3. Define the Table Name and Primary Key:

Table name: Enter a name for your table, such as SensorData.

Partition key: This key is unique for each entry. For sensor data, you can use something like DeviceID or SensorID as the partition key. Set the Data type as String.

You can optionally define a Sort key if you want to sort the data. For example, you can use Timestamp as a sort key (data type String or Number).



4. Configure Read and Write Capacity Settings:

You can leave the default settings for capacity mode as On-demand (recommended for unpredictable traffic).

Alternatively, you can set the table to Provisioned if you want to manually manage read/write capacity units.



5. Add Tags (Optional):

You can add tags to organize your DynamoDB resources, but this is optional.



6. Enable Encryption (Optional):

Encryption is enabled by default using AWS-managed keys. You can leave this setting as is.



7. Create the Table:

Click Create table. The table creation will take a few seconds.





---

## Step 2: Define Table Schema (Attributes)

Once the table is created, you can add additional attributes to store specific sensor data, such as temperature, humidity, gas levels, etc.

1. Add Attributes:

Each item in the table will consist of the attributes you define. These are examples of the attributes you might want to add:

DeviceID (Primary Partition Key)

Timestamp (String or Number for tracking the time of the data collection)

Temperature (Number)

Humidity (Number)

GasLevel (Number)

Status (String – e.g., On, Off, or any other status for devices connected to relays)




2. Data Types:

DynamoDB supports several data types, including String, Number, Boolean, and Binary. Make sure you select the correct data types for each attribute based on the sensor data.





---

## Step 3: Create and Configure IAM Roles for DynamoDB Access

Your ESP32 (via AWS IoT Core) and Lambda function will need to access the DynamoDB table, so you must create an IAM role or user with the appropriate permissions.

1. Go to AWS IAM Console:

Open the IAM (Identity and Access Management) console.

Click on Roles → Create role.



2. Select Trusted Entity:

Select AWS service as the trusted entity.

Choose Lambda (if you plan to use a Lambda function to read/write data to DynamoDB).



3. Attach Policies:

Search for the policy AmazonDynamoDBFullAccess and attach it. This gives full access to your Lambda function or IoT device to read and write to DynamoDB.



4. Complete the Role Creation:

Name the role (e.g., DynamoDBAccessRole).

Click Create role.



5. Attach the Role to Lambda/IoT:

If you're using a Lambda function to process or store data, make sure this role is attached to the Lambda function in the Permissions section.





---

## Step 4: Write Data to DynamoDB from ESP32

Once the table is created and permissions are set up, you need to write the program to send sensor data from the ESP32 to AWS IoT Core, and then use an AWS Lambda function to store the data in the DynamoDB table.

ESP32 Code to Send Data to AWS IoT Core

Make sure your ESP32 is configured to communicate with AWS IoT Core. You need to publish the sensor data to an MQTT topic in AWS IoT Core. Here's a sample code to send temperature, humidity, and gas sensor data:
```
#include <WiFi.h>
#include <MQTTClient.h>
#include <AWS_IOT.h>

AWS_IOT hornbill;

char WIFI_SSID[] = "your_wifi_ssid";
char WIFI_PASSWORD[] = "your_wifi_password";

char HOST_ADDRESS[] = "your_aws_endpoint.iot.us-west-2.amazonaws.com";
char CLIENT_ID[] = "esp32_client_id";
char TOPIC_NAME[] = "esp32/sensordata";

void setup() {
    Serial.begin(115200);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("WiFi connected.");
    
    if (hornbill.connect(HOST_ADDRESS, CLIENT_ID) == 0) {
        Serial.println("Connected to AWS IoT.");
    } else {
        Serial.println("AWS IoT connection failed.");
    }
}

void loop() {
    // Example sensor data
    float temperature = analogRead(34);  // Replace with actual sensor reading
    float humidity = analogRead(35);
    float gas = analogRead(36);
    
    // Prepare data to send
    char payload[512];
    snprintf(payload, sizeof(payload), "{\"temperature\": %.2f, \"humidity\": %.2f, \"gas\": %.2f}", temperature, humidity, gas);
    
    // Publish data to AWS IoT
    if (hornbill.publish(TOPIC_NAME, payload) == 0) {
        Serial.println("Data published.");
    } else {
        Serial.println("Data publishing failed.");
    }
    
    delay(5000);  // Send data every 5 seconds
}
```

AWS Lambda Function to Store Data into DynamoDB

Once the data is published to AWS IoT, you can create an IoT Rule to trigger a Lambda function that writes the sensor data into DynamoDB.

1. Go to AWS IoT Core Console:

Go to IoT Core → Act → Create a Rule.



2. Define Rule Action:

Select DynamoDB or Lambda as the action.

Choose Lambda if you want to use a function to process the data before saving.



3. Create Lambda Function to Insert Data:



Here is an example of a Python Lambda function that stores sensor data into the DynamoDB table:
```
import json
import boto3
import time

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Replace with your DynamoDB table name
table_name = "SensorData"
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Extract sensor data from the incoming event
    try:
        data = json.loads(event['Records'][0]['Sns']['Message'])
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        gas_level = data.get('gas')
        
        # Get current timestamp
        timestamp = int(time.time())
        
        # Store the data in DynamoDB
        table.put_item(
            Item={
                'DeviceID': 'ESP32-001',
                'Timestamp': str(timestamp),
                'Temperature': temperature,
                'Humidity': humidity,
                'GasLevel': gas_level
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data stored successfully.')
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error storing data: {str(e)}")
        }
```
## Step 5: Trigger Lambda from AWS IoT Rule

1. Go to IoT Core → Act → Rules.


2. Create a rule that triggers the Lambda function when a message is published to the topic (e.g., esp32/sensordata).


3. This will enable real-time processing of data and storage in DynamoDB.




---

Summary

Create DynamoDB Table: Set up the table with DeviceID as the partition key, and other attributes like temperature, humidity, etc.

ESP32 Publishes Data to IoT Core: Program your ESP32 to send sensor data to AWS IoT Core.

IoT Rule: Configure an IoT rule to trigger a Lambda function when data is published.

Lambda Function: Write a Lambda function to store the sensor data into DynamoDB.

Monitor: Use CloudWatch or DynamoDB Streams for real-time monitoring of the data.


This configuration enables you to store sensor data into DynamoDB and process it for further analysis or triggering notifications based on thresholds.


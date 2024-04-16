# Main controller
from time import sleep
import temperature as temp
import humidity as humi
import paho.mqtt.client as mqtt
import json

# MQTT server details
mqtt_start = False
MQTT_BROKER = "185.148.12.45"
MQTT_PORT = 1883 # use 8883 if communication should be encrypted
MQTT_TOPIC = "test/topic"
USERNAME = "username"
PASSWORD = "password"



def fetch_data_sense_hat():
    temperature = temp.read_temperature()
    humidity =  humi.read_humidity()
    print(f"Reading temperature: {temperature}C")

    print(f"Reading humidity: {humidity}%")
    return temperature, humidity

# Callback when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully.")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}\n")
# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

def init_mqtt_client(client):
    # Set username and password
    client.username_pw_set(USERNAME, PASSWORD)

    # Assign callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    # TODO maybe implement on_disconnect and on_subscribe

    # Connect to the MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT)

def send_readings(message):
    # Publish message on MQTT_TOPIC
    client.publish(MQTT_TOPIC, "Hello MQTT")

if __name__ == "__main__":
    if mqtt_start:
        # Create MQTT client
        client = mqtt.Client()
        init_mqtt_client(client)

    while True:
        temperature, humidity = fetch_data_sense_hat()
        sleep(1)
        # DATA in JSON format
        data = {
            "Temperature": temperature,
            "Humidity": humidity
        }
        # Convert data to JSON
        json_data = json.dumps(data)
        send_readings(json_data)
        sleep(4)

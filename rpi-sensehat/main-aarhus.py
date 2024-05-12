# Main controller
from time import sleep
import time
import temperature.temperature as temp
import humidity.humidity as humi
import colour.colour as col
import pressure.pressure as pre
import paho.mqtt.client as mqtt
from sense_emu import SenseHat
import json

# MQTT server details
mqtt_start = True
MQTT_BROKER = "mqtt.niels-bjorn.dk"
MQTT_PORT = 1883  # use 8883 if communication should be encrypted
MQTT_TOPIC = "test/topic"
MQTT_LAST_WILL_TOPIC = "status/raspberry-aarhus/connection"
USERNAME = "rpimqttclienta"
PASSWORD = "pD2l0bYEw"


def init_mqtt_client(client):
    # Set username and password
    client.username_pw_set(USERNAME, PASSWORD)

    # Assign callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    # TODO maybe implement and on_subscribe

    # Last will message
    last_will_message = "OFF"
    client.will_set(MQTT_LAST_WILL_TOPIC, payload=last_will_message, qos=1, retain=True)

    # Connect to the MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT)


def fetch_data_sense_hat(sense):
    # col.set_settings_for_colour_sensing(sense, 60, 64)
    # red, green, blue = col.read_colours(sense)
    # brightness = col.read_brightness(sense)

    # Get sensor data
    pressure = pre.read_pressure(sense)
    temperature = temp.read_temperature(sense)
    humidity = humi.read_humidity(sense)

    # Get the current Unix timestamp
    current_timestamp = time.time()

    # Dictionary containing the sensor data
    data = {
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'timestamp': current_timestamp,
        'location': 'aarhus'
        #       "brightness" : brightness,
        #       "red" : red,
        #       "green" : green,
        #       "blue" : blue
    }
    return data


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
        # Attempt to reconnect
        try:
            print("Trying to reconnect...")
            client.reconnect()
        except Exception as e:
            print(f"Reconnection failed: {e}")
    else:
        print("Disconnected successfully.")


# Callback when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully.")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(MQTT_TOPIC)

        # Set status for the raspberry
        client.publish(MQTT_LAST_WILL_TOPIC, "ON", retain=True)
    else:
        print(f"Failed to connect, return code {rc}\n")


# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")


def send_readings(topic, message):
    # Publish sensor values on MQTT_TOPIC
    client.publish(topic + "/all_readings", str(message))


if __name__ == "__main__":
    sense = SenseHat()
    sense.clear()
    if mqtt_start is False:
        while True:
            data = fetch_data_sense_hat(sense)
            # print(data[1])
            print(data["temperature"], data["humidity"])
            sleep(4)

    if mqtt_start:
        # Create MQTT client
        client = mqtt.Client()
        print("initialize MQTT")
        init_mqtt_client(client)

    if mqtt_start:
        client.loop_start()
        while True:
            data = fetch_data_sense_hat(sense)
            send_readings("raspberry/Aarhus/sense-hat/readings", data)
            sleep(5)

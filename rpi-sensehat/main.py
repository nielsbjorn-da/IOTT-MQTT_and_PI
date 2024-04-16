# Main controller
from time import sleep
import temperature.temperature as temp
import humidity.humidity as humi
import colour.colour as col
import pressure.pressure as pre
import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import json

# MQTT server details
mqtt_start = False
MQTT_BROKER = "185.148.12.45"
MQTT_PORT = 1883 # use 8883 if communication should be encrypted
MQTT_TOPIC = "test/topic"
MQTT_LAST_WILL_TOPIC = "raspberry/status"
USERNAME = "username"
PASSWORD = "password"



def fetch_data_sense_hat(sense):
    col.set_settings_for_colour_sensing(sense, 60, 64)
    red, green, blue = col.read_colours(sense)
    brightness = col.read_brightness(sense)
    pressure = pre.read_pressure(sense)
    temperature = temp.read_temperature(sense)
    humidity =  humi.read_humidity(sense)
    print(f"Reading temperature: {temperature}C")
    print(f"Reading humidity: {humidity}%")
    print(f"Reading pressure: {pressure}")
    print(f"Reading brightness: {brightness}")
    print(f"Reading colours: Red = {red}, Green = {green}, Blue = {blue}")

    # use dictionary to store data
    data = {
        "temperature" : temperature,
        "humidity" : humidity,
        "pressure" : pressure,
        "brightness" : brightness,
        "red" : red,
        "green" : green,
        "blue" : blue
    }
    return data

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
    client.publish("raspberry/sense-hat/readings/all_readings", message)
    client.publish("raspberry/sense-hat/readings/temperature", message["temperature"])
    client.publish("raspberry/sense-hat/readings/humidity", message["humidity"])
    client.publish("raspberry/sense-hat/readings/pressure", message["pressure"])
    client.publish("raspberry/sense-hat/readings/brightness", message["brightness"])
    client.publish("raspberry/sense-hat/readings/colour_red", message["red"])
    client.publish("raspberry/sense-hat/readings/colour_green", message["green"])
    client.publish("raspberry/sense-hat/readings/colour_blue", message["blue"])


if __name__ == "__main__":
    sense = SenseHat()
    if mqtt_start is False:
        while True:
            data = fetch_data_sense_hat(sense)
            #print(data[1])
            print(data["temperature"], data["humidity"])
            sleep(4)
    
    if mqtt_start:
        # Create MQTT client
        client = mqtt.Client()
        init_mqtt_client(client)

    if mqtt_start:
        while True:
            data = fetch_data_sense_hat(sense)
            sleep(1)
            # Convert data to JSON
            json_data = json.dumps(data)
            send_readings(json_data)
            sleep(4)

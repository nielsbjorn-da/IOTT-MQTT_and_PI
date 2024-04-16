# Main controller
from time import sleep
import temperature.temperature as temp
import humidity.humidity as humi
import colour.colour as col
import pressure.pressure as pre
import paho.mqtt.client as mqtt
from sense_emu import SenseHat #from sense_hat import SenseHat
import json

# MQTT server details
mqtt_start = True
MQTT_BROKER = "mqtt.niels-bjorn.dk"
MQTT_PORT = 1883 # use 8883 if communication should be encrypted
MQTT_TOPIC = "test/topic"
MQTT_LAST_WILL_TOPIC = "raspberry/status"
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
    last_will_message = "Client " + USERNAME + " has disconnected"
    client.will_set(MQTT_LAST_WILL_TOPIC, payload=last_will_message, qos=1, retain=False)

    # Connect to the MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT)

def fetch_data_sense_hat(sense):
    #col.set_settings_for_colour_sensing(sense, 60, 64)
    #red, green, blue = col.read_colours(sense)
    #brightness = col.read_brightness(sense)
    pressure = pre.read_pressure(sense)
    temperature = temp.read_temperature(sense)
    humidity =  humi.read_humidity(sense)
    #print(f"Reading temperature: {temperature}C")
    #print(f"Reading humidity: {humidity}%")
    #print(f"Reading pressure: {pressure}")
    #print(f"Reading brightness: {brightness}")
    #print(f"Reading colours: Red = {red}, Green = {green}, Blue = {blue}")

    # use dictionary to store data
    data = {
        "temperature" : temperature,
        "humidity" : humidity,
        "pressure" : pressure
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
    else:
        print(f"Failed to connect, return code {rc}\n")

# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")


def send_readings(topic, message):
    # Publish message on MQTT_TOPIC

    client.publish(topic + "/all_readings", str(message))
    client.publish(topic + "/temperature", str(message["temperature"]))
    client.publish(topic + "/humidity", str(message["humidity"]))
    client.publish(topic + "/pressure", str(message["pressure"]))
    #client.publish("raspberry/sense-hat/readings/brightness", message["brightness"])
    #client.publish("raspberry/sense-hat/readings/colour_red", message["red"])
    #client.publish("raspberry/sense-hat/readings/colour_green", message["green"])
    #client.publish("raspberry/sense-hat/readings/colour_blue", message["blue"])


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
        print("initialize MQTT")
        init_mqtt_client(client)

    if mqtt_start:
        client.loop_start()
        while True:
            data = fetch_data_sense_hat(sense)
            send_readings("raspberry/Aarhus/sense-hat/readings", data)
            sleep(3)
            data = fetch_data_sense_hat(sense)
            send_readings("raspberry/Aalborg/sense-hat/readings",data)
            sleep(3)
            data = fetch_data_sense_hat(sense)
            send_readings("raspberry/Copenhagen/sense-hat/readings",data)
            sleep(3)
            data = fetch_data_sense_hat(sense)
            send_readings("raspberry/Silkeborg/sense-hat/readings",data)
            sleep(3)
            data = fetch_data_sense_hat(sense)
            send_readings("raspberry/Odense/sense-hat/readings",data)
            sleep(10)

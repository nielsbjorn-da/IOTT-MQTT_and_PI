from sense_hat import SenseHat

def read_temperature():
    sense = SenseHat()
    temperature = sense.get_temperature()
    print(f"Temperature from the subscript: {temperature}C")
    return temperature
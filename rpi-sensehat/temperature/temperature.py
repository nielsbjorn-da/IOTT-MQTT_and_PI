def read_temperature(sense):
    temperature = sense.get_temperature()
    #print(f"Temperature from the subscript: {temperature}C")
    return temperature
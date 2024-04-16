def read_humidity(sense):
    # sense = SenseHat()
    humidity = sense.get_humidity()
    #print(f"Humidity from the subscript: {humidity}%")
    return humidity

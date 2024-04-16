def read_pressure(sense):
    sense.clear()
    pressure = sense.get_pressure()
    return pressure
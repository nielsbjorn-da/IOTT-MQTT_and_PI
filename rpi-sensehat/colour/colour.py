def set_settings_for_colour_sensing(sense, gain, integration_cycles):
    if gain is None:
        sense.color.gain = 60 # Gain is simply the sensitivity of the sensor
    if integration_cycles is None:
        sense.color.integration_cycles = 64 # Integration cycles is the sensor takes between measuring the light
        # Each integration cycle is 2.4 milliseconds long

    return sense

def get_colours(sense):
    red, green, blue, clear = sense.colour.colour # Each colour is an integer between 0 and 255

    return  red, green, blue

def get_brightness(sense):
    red, green, blue, brightness = sense.colour.colour
    return brightness


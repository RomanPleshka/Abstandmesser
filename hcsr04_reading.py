from hcsr04 import HCSR04
import json

sensor = HCSR04(trigger_pin=0, echo_pin=2)

def returnDistance():
    distance = sensor.distance_cm()
    return distance
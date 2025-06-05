from hcsr04 import HCSR04
from machine import Pin, Timer

sensor = HCSR04(trigger_pin=0, echo_pin=16)
led = Pin(2, Pin.OUT)

timer = Timer(-1)


def ledOff(t):
    """
    Diese Funktion wird als Callback für den Timer verwendet.
    Sie schaltet die LED wieder aus.

    Args:
        t (Timer): Der Timer, der die Funktion aufruft (nicht verwendet).
    """
    led(1)

def blinkLed():
    """
    Schaltet die LED kurz an und wieder aus.

    Die LED wird auf LOW (an) gesetzt, dann startet ein One-Shot-Timer,
    der nach 1 Sekunde die Funktion `ledOff` aufruft, um sie wieder auszuschalten.
    """
    led(0)
    timer.init(period=1000, mode=Timer.ONE_SHOT, callback=ledOff)

def returnDistance():
    """
    Misst die Distanz mithilfe des Sensors sowie der HCSR04 Bibliothek und gibt diese zurück.
    Die gemessene Distanz wird in Zentimetern ausgegeben und zurückgegeben.
    Nach der Messung blinkt die LED kurz auf.

    Returns:
        float: Die gemessene Distanz in Zentimetern.
    """
    distance = sensor.distance_cm()
    blinkLed()
    print(f"{distance} cm")
    return distance

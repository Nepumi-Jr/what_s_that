from machine import Pin
from time import sleep
from src.service.config import get_config

soundPin = Pin(get_config().soundSensor.out, Pin.IN)

def soundSensor():
    return soundPin.value()
from machine import Pin, ADC
from time import sleep
from src.service.config import get_config

config = get_config()
if config.soundSensor.is_analog:
    soundPin = ADC(Pin(config.soundSensor.out))
    soundPin.atten(ADC.ATTN_11DB)
    soundPin.width(ADC.WIDTH_12BIT) # 0-4095
else:
    soundPin = Pin(config.soundSensor.out, Pin.IN)

def soundSensor():
    """ออกมาเป็น 0 - 1 โดยเป็น Active Low"""
    if config.soundSensor.is_analog:
        return soundPin.read() / 4095
    return soundPin.value()
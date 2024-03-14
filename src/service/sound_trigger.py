from src.hardware.sound_sensor import soundSensor

def soundTrigger(funMode: bool):
    if(funMode and soundSensor() == 1):
        return True
    else:
        return False
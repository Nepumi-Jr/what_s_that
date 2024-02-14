from machine import Pin

buttonPinMap = {}

def assign_pin(buttonInd : int, pin : int):
    buttonPinMap[buttonInd] = Pin(pin, Pin.IN)

def is_press(buttonInd : int) -> bool:
    return buttonPinMap[buttonInd].value() == 0
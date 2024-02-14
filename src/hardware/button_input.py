from machine import Pin

buttonPinMap = {}

def assign_pin(buttonInd : int, pin : Pin):
    #TODO : ไปเพิ่ม  setting Input อะไรสักอย่างของอี Machine
    buttonPinMap[buttonInd] = pin

def is_press(buttonInd : int) -> bool:
    #TODO : ไปเพิ่ม การเช็คว่ามันกดหรือยัง
    pass
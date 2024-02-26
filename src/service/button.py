from machine import Pin
from src.service import config
from src.hardware import button_input as b_in

HOLD_SEC = 2
DEBOUNCE_SEC = 0.1

buttons = []
stateButton = {}
timeDelay = {}
isCalled = {}

def assign_pin(buttonInd : int, pin : int):
    b_in.assign_pin(buttonInd, pin)
    stateButton[buttonInd] = 0
    timeDelay[buttonInd] = 0
    buttons.append(buttonInd)

config = config.get_config()
assign_pin(0, config.button.button1)
assign_pin(1, config.button.button2)
assign_pin(2, config.button.button3)
if config.button.button4 != None:
    assign_pin(3, config.button.button4)

def get_button_number() -> int:
    return len(buttons)

def is_first_press(buttonInd : int) -> bool:
    if stateButton[buttonInd] == 1 and not isCalled[buttonInd]:
        isCalled[buttonInd] = True
        return True
    return False

def is_hold(buttonInd : int) -> bool:
    return stateButton[buttonInd] == 3

# state will handle here
# to see description of state, see GoodNote กู
def clock_tick(dSec : float):
    for button in buttons:
        state = stateButton[button]

        if state == 0: # wait or idle
            if b_in.is_press(button):
                stateButton[button] = 1
                timeDelay[button] = HOLD_SEC
                isCalled[button] = False
        elif state == 1:# first press
            if b_in.is_press(button) and timeDelay[button] == 0:
                stateButton[button] = 3
            elif not b_in.is_press(button) and isCalled[button]:
                stateButton[button] = 2
                timeDelay[button] = DEBOUNCE_SEC
        elif state == 2: # debounce
            if timeDelay[button] == 0:
                stateButton[button] = 0
        elif state == 3: # hold
            if not b_in.is_press(button):
                stateButton[button] = 2
        
        if timeDelay[button] > 0:
            timeDelay[button] = max(timeDelay[button] - dSec, 0)
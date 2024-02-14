from machine import Pin
from src.hardware import button_input as b_in

HOLD_SEC = 2
DEBOUNCE_SEC = 0.1

buttons = []
stateButton = {}
timeDelay = {}
isCalled = {}


def assign_pin(buttonInd : int, pin : Pin):
    button_input.assign_pin(buttonInd, pin)
    stateButton[buttonInd] = 0
    buttons.append(buttonInd)

def is_first_press(buttonInd : int) -> bool:
    if stateButton[buttonInd] == 1:
        isCalled[buttonInd] = True
        return True
    return False

def is_hold(buttonInd : int) -> bool:
    return stateButton[buttonInd] == 3

# state will handle here
# to see description of state, see GoodNote กู
def clock_tick():
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
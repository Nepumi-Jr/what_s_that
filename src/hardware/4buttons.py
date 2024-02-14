from machine import Pin
from time import sleep

push_button_red = Pin(16, Pin.IN)
push_button_yellow = Pin(17, Pin.IN)
push_button_blue = Pin(26, Pin.IN)
push_button_green = Pin(27, Pin.IN)
buttons = [push_button_red,push_button_yellow,push_button_blue,push_button_green]

while True:
    for button in buttons:
        if button.value():     # if pressed the push_button
          print(button.value())             # led will turn ON
        else:                       # if push_button not pressed
          print(button.value())             # led will turn OFF
    sleep(2)

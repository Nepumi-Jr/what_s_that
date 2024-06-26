from src.util import log
import tm1637
from src.service.config import get_config
from machine import Pin

config = get_config()
tm = tm1637.TM1637(clk=Pin(get_config().digitDisp.clock), dio=Pin(get_config().digitDisp.data))


def on_display(second_remaining : float, force_colon = False):
    

    second = second_remaining % 60
    minute = int(second_remaining / 60)
    if((second_remaining % 1) < 0.50) or force_colon: 
        colon = True
    else :
        colon = False
        
    tm.numbers(minute, int(second), colon)

def clear():
    tm.write(bytearray(b'\x00\x00\x00\x00'))
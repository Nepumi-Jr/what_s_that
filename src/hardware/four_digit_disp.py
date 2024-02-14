from src.util import log
import tm1637
from machine import Pin




def on_display(second_remaining : float):
    tm = tm1637.TM1637(clk=Pin(26), dio=Pin(27))

    second = second_remaining % 60
    minute = int(second_remaining / 60)
    if((second_remaining % 1) < 0.50): 
        colon = True
    
    else :
        colon = False
        
    
    tm.numbers(minute, int(second), colon)
    
    pass
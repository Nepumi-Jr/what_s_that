from src.hardware import four_digit_disp

time_use = 0

def clear():
    four_digit_disp.clear()

def reset(initTime:float = 0):
    global time_use
    time_use = initTime

def count_tick_time(dSecond : float = 1/15):
    global time_use
    time_use += dSecond
    four_digit_disp.on_display(time_use)
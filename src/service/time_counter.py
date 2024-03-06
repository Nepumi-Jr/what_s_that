from src.hardware import four_digit_disp

time_use = 0

def reset():
    global time_use
    time_use = 0

def count_tick_time(dSecond : float = 1/15):
    global time_use
    time_use += dSecond
    four_digit_disp.on_display(time_use)
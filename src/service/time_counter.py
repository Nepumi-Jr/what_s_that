from src.hardware import four_digit_disp

time_use = 0

def reset():
    global second_remaining
    second_remaining = 0

def count_tick_time(dSecond : float = 1/15):
    global second_remaining
    second_remaining += dSecond
    if second_remaining < 0:
        second_remaining = 0
    four_digit_disp.on_display(second_remaining)
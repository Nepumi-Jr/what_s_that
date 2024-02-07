from src.hardware import four_digit_disp

second_remaining = 0

def set_second_remaining(second : float):
    global second_remaining
    second_remaining = second

def decrease_second_remaining(dSecond : float = 1/15):
    global second_remaining
    second_remaining -= dSecond
    if second_remaining < 0:
        second_remaining = 0
    four_digit_disp.on_display()

def is_time_up() -> bool:
    return second_remaining == 0
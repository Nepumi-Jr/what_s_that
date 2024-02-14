from src.service import time_counter, button
from src import game_settings
from src.util import log
from time import sleep


FRAME_RATE = 15


def main():

    time_counter.reset()
    time_limit = game_settings.number_of_stage * 10 * 60 # 10 minute per stage
    button.assign_pin(0,26)
    while time_counter.time_use < time_limit:
        if(button.is_first_press(0)): print("HEE")
        if(button.is_hold(0)): print("HUM")
        # decrease the time, disp and wait
        time_counter.count_tick_time( 1 / FRAME_RATE)
        button.clock_tick(1 / FRAME_RATE)
        sleep(1 / FRAME_RATE)
    
    print("Time's up!")
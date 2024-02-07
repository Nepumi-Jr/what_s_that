from src.service import time_counter
from src import game_settings
from time import sleep

FRAME_RATE = 15

def test():
    print(f"Setting {game_settings.sample}")

def main():
    time_counter.set_second_remaining(game_settings.init_time)
    while not time_counter.is_time_up():

        

        # decrease the time, disp and wait
        time_counter.decrease_second_remaining( 1 / FRAME_RATE)
        sleep(1 / FRAME_RATE)
    
    print("Time's up!")
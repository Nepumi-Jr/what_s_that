from src.service import time_counter, morse
from src import game_settings
from src.util import log
from time import sleep

FRAME_RATE = 15

def test():
    print(f"Setting {game_settings.sample}")

def main():

    time_counter.set_second_remaining(game_settings.init_time)
    morse.set_word("CAT")
    log.debug(">>>>",morse.curWordMorse)
    while not time_counter.is_time_up():

        morse.cur_morse_signal()

        # decrease the time, disp and wait
        morse.reload_morse(1 / FRAME_RATE)
        time_counter.decrease_second_remaining( 1 / FRAME_RATE)
        sleep(1 / FRAME_RATE)
    
    print("Time's up!")
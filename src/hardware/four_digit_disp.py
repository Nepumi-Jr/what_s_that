from src.util import log

def on_display(second_remaining : float):
    # TODO: use TM1637 to display the remaining time
    log.debug(f"Time remaining: {second_remaining:.2f}")
    pass
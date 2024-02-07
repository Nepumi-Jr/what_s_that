from src import game_settings
from src.util import log

# Morse code dictionary
morseCode = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..'}


curWord = ""
curWordMorse = ""
curCharIndex = 0
timeRemaining = 0

def set_word(word : str):
    global curWord, curWordMorse, curCharIndex
    curWord = word
    curWordMorse = '|'.join([','.join(morseCode[c.upper()]) for c in word]) + ' '
    curCharIndex = 0

def set_char_ind(ind : int):
    global curCharIndex, timeRemaining
    curCharIndex = ind
    if curWordMorse[curCharIndex] == '|':
        timeRemaining = game_settings.space_duration
    elif curWordMorse[curCharIndex] == ' ':
        timeRemaining = game_settings.word_space_duration
    elif curWordMorse[curCharIndex] == '.' or curWordMorse[curCharIndex] == ',':
        timeRemaining = game_settings.dot_duration
    else:
        timeRemaining = game_settings.dash_duration

def set_next_char():
    global curCharIndex, timeRemaining
    curCharIndex += 1
    curCharIndex %= len(curWordMorse)
    set_char_ind(curCharIndex)

def reload_morse(dSecond : float):
    global curCharIndex, timeRemaining
    timeRemaining -= dSecond
    if timeRemaining < 0:
        timeRemaining = 0
        set_next_char()

def cur_morse_signal() -> bool:
    if curWordMorse[curCharIndex] not in "| ,":
        log.debug("######")
    else:
        log.debug("      ")
    return curWordMorse[curCharIndex] not in "| ,"
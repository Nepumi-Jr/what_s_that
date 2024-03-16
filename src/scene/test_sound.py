#from src.hardware import sound_sensor as sound
from src.service import sound_trigger as sound
from time import sleep

# def main():
#     while True:
#         volume = round(sound.soundSensor() * 10)
#         sstr = ""
#         for i in range(10):
#             if i < volume:
#                 sstr += "#"
#             else:
#                 sstr += " "
#         print(sstr, int(sound.soundSensor()*1000))
#         sleep(0.05)

FRAME_RATE = 30


def main():
    while True:
        soundAvg = sound.getSoundAvg()
        print(int(soundAvg*1000))
        
        sound.reload_sound_loop()
        sleep(1/FRAME_RATE)

if __name__ == "__main__":
    main()
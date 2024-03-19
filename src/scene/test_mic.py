from src.service import oled_lcd, oled_nevigate, button
from src.service import sound_trigger as sound
from src.service.oled_lcd import TextAlign
from src.service.scene import SCENE as scene
from time import sleep, time_ns

FRAME_RATE = 30

def main():
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setAllButtonIcon(oled_nevigate.Icon.BACK)
    
    oled_lcd.textInLine("Test Mic", oled_lcd.CenterX(), 0, TextAlign.CENTER)
    oled_lcd.textInLine("show me ya voice", oled_lcd.CenterX(), 4, TextAlign.CENTER)
    oled_lcd.text("[", oled_lcd.CenterX() - 20 - 8, oled_lcd.CenterY() - 4)
    oled_lcd.text("]", oled_lcd.CenterX() - 20 + 45 + 8, oled_lcd.CenterY() - 4)
    
    sound.reset_queue()
    pSound = 0
    max_sound = 0
    time_sound = 9999
    while True:
        max_sound = max(max_sound, sound.getSoundvolume())
        sound.reload_sound_loop()
        if time_sound > 1 / FRAME_RATE: #? loop in FRAME_RATE
            if(button.is_first_press(0)) or (button.is_first_press(1)) or (button.is_first_press(2)) or (button.is_first_press(3)):
                return scene.MENU
            

            SOUND_THR = 0.3
            this_sound = round(min(max_sound / SOUND_THR, 1)  * 10)
            if this_sound >= pSound:
                for i in range(pSound, this_sound):
                    oled_lcd.rect(oled_lcd.CenterX() - 17 + 5 * i, oled_lcd.CenterY() + 2, oled_lcd.CenterX() - 17 + 5 * i + 3, oled_lcd.CenterY() + 2 - max(2, (i * 5 // 9)))
            else:
                for i in range(this_sound, pSound):
                    oled_lcd.delRect(oled_lcd.CenterX() - 17 + 5 * i, oled_lcd.CenterY() + 2, oled_lcd.CenterX() - 17 + 5 * i + 3, oled_lcd.CenterY() + 2 - max(2, (i * 5 // 9)))
            oled_lcd.show()
            pSound = this_sound
            button.clock_tick(1 / FRAME_RATE)
            time_sound = 0
            max_sound = 0
        time_sound += 0.005
        sleep(0.005)

if __name__ == "__main__":
    main()

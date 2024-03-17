from src.service import button, oled_lcd, oled_nevigate
from src.service.scene import SCENE as scene
from time import sleep, time_ns

def main():
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setAllButtonIcon(oled_nevigate.Icon.CONFIRM)

    oled_lcd.textInLine("Game Over", oled_lcd.CenterX(), 1, oled_lcd.TextAlign.CENTER)
    oled_lcd.textInLine("Thank 4 playing", oled_lcd.CenterX(), 4, oled_lcd.TextAlign.CENTER, True)

    while True:
        if button.is_first_press(0) or button.is_first_press(1) or button.is_first_press(2) or button.is_first_press(3):
            return scene.MENU
        button.clock_tick(1 / 30)
        sleep(1 / 30)

if __name__ == "__main__":
    main()
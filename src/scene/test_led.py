# กูทดสอบสึ ๆ ว่า UART มันเฮ็ดงานได้บ่
from src.service import oled_lcd as oled
from src.service.oled_lcd import TextAlign
from src.service import oled_nevigate as oled_nav
from src.service import uart, config, button
from time import sleep

def main():
    oled.clear(False)
    oled_nav.reset()
    oled_nav.setButtonIcon(2, oled_nav.Icon.BACK)
    oled.textInLine("Just test :D", oled.CenterX(), 0, TextAlign.CENTER, False)
    oled.textInLine("RED_LED : Off", oled.CenterX(), 1, TextAlign.CENTER, False)
    oled.textInLine("WHITE_LED : ????", oled.CenterX(), 2, TextAlign.CENTER, True)
    redLed = False

    while True:
        readData = uart.read()
        if readData == "WhiteOn":
            oled.textInLine("WHITE_LED : On", oled.CenterX(), 2, TextAlign.CENTER, True)
        elif readData == "WhiteOff":
            oled.textInLine("WHITE_LED : Off", oled.CenterX(), 2, TextAlign.CENTER, True)
        if button.is_first_press(2):
            redLed = not redLed
            while not uart.send("Red" + ("On" if redLed else "Off")):
                sleep(0.01)
            oled.textInLine("RED_LED : " + ("On" if redLed else "Off"), oled.CenterX(), 1, TextAlign.CENTER, True)
        
        button.clock_tick(0.01)
        sleep(0.01)

if __name__ == "__main__":
    main()

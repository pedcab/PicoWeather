import machine
import time
import math
from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

lcd.backlight_on()
time.sleep_ms(250)
lcd.backlight_off()
time.sleep_ms(250)
lcd.backlight_on()
zerotime=time.time()

while (True):
    lcd.putstr(" ") #clear screen
    elapsedTime = (time.time() - zerotime) #zero time
    
    secs = elapsedTime % 60
    min = elapsedTime // 60 % 60
    hour = elapsedTime // 60 // 60

    lcd.move_to(0,0)
    lcd.putstr(str(hour) + ":" + str(min) + ":" + str(secs))
    
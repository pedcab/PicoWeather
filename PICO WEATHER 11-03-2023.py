import machine
import time
import math
from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

file=open("logtime.txt","r")   #open txt file in read mode

previousTimeLogRead = str(file.read()) #read contents of the log file

if previousTimeLogRead == "": #evaluate if file is empty 
   previousTimeLog=1 #give a value of second if file is empty (to avoid crash on adding log value to an empty file)
else:
    previousTimeLog= previousTimeLogRead #if fine not empty read give its content to tjhe previous log variable
    
print(previousTimeLog)

file.close()

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
    file=open("logtime.txt","w")   #open txt file in write mode
    lcd.putstr(" ") #clear screen
    elapsedTime = (time.time() - zerotime) #zero time
    secs = elapsedTime % 60
    mins = elapsedTime // 60 % 60
    hour = elapsedTime // 60 // 60
    
    totalTimeLog = int(previousTimeLog) + elapsedTime
    logSecs = totalTimeLog % 60
    logMin = totalTimeLog // 60 % 60
    logHour = totalTimeLog // 60 // 60

    lcd.move_to(0,0)
    lcd.putstr(str(hour) + ":" + str(mins) + ":" + str(secs) +
               "   " + str(logHour) + ":" + str(logMin) + ":" + str(logSecs))
    
    totalTimeLog=int(previousTimeLog)+elapsedTime
    
    
    file.write(str(totalTimeLog))  #write data point to file
    time.sleep(0.1)
    #file.flush()    #internal buffer flush
    file.close()    #file close
    
    
    
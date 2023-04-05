#MODULES & LIBRARIES
import machine
import time
import math
from machine import ADC, Pin, PWM, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

#CIRCUIT
    #LDR
        #3.3V to LDR to 1.8k to GROUND
        #Division point to pin 34 (ADC 2)
    #BUS VOLTAGE
        #Bus voltage to 100k to 10k to ground
        #Division point to pin 32 (ADC 1)

#I2C LCD CONTROL SETUP
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#I/O OBJECTS
lcdLed = PWM(Pin(2, mode=Pin.OUT)) #LCD LED output object
ldr = ADC(Pin(28, mode=Pin.IN)) #LDR input object
busVoltSensor = ADC(Pin(27, mode=Pin.IN)) #bus voltage object
cpuTempSensor = machine.ADC(4) #get internal temp value from adc 4
extTempSensor = ADC(Pin(26, mode=Pin.IN)) #External temperature sensor object

#LOG FILE HANDLING
file=open("logtime.txt","r")   #open txt file in read mode
previousTimeLogRead = str(file.read()) #read contents of the log file
if previousTimeLogRead == "": #evaluate if file is empty 
   previousTimeLog=1 #give a value of 1 second if file is empty (to avoid crash on adding log value to an empty file)
else:
    previousTimeLog= previousTimeLogRead #if file not empty attribute its stored value to previous log variable
file.close()

#GET ZERO TIME ELAPSED VALUE
zerotime=time.time()

#LOOP
while (True):
    #LCD CLEAR
    lcd.move_to(0,0)
    lcd.putstr("")
    lcd.move_to(0,1)
    lcd.putstr("")
    lcd.move_to(0,2)
    lcd.putstr("")
    lcd.move_to(0,3)
    lcd.putstr("")  

    #TIME LOG OPERATIONS
    file=open("logtime.txt","w")   #open txt file in write mode
    elapsedTime = (time.time() - zerotime) #zero time
    secs = elapsedTime % 60 #seconds elapsed from last power up
    mins = elapsedTime // 60 % 60 #minutes elapsed from last power up
    hour = elapsedTime // 60 // 60 #hours elapsed from last power up
    totalTimeLog = int(previousTimeLog) + elapsedTime #total log time elapsed
    logHour = totalTimeLog // 60 // 60 #hours elapsed from last file reset
    lcd.move_to(5,3) #lcd cursor to column 0 line 0
    lcd.putstr(str(hour) + "h" + str(mins) + "m") #print time elapsed to lcd
    lcd.move_to(12,3) #lcd cursor
    lcd.putstr(str(logHour)+"h") #print total log hours to lcd
    totalTimeLog=int(previousTimeLog)+elapsedTime #add time elapsed to time log
    file.write(str(totalTimeLog))  #write data point to file
        
    #SENSOR BASED OPERATIONS
        #TEMPERATURE  
            #CPU
    cpuTemp = int(((cpuTempSensor.read_u16() * 3.3 / 65535) * 27) / 0.706) #calculate cpu temp (3.3 volts/65535 points and RPI pico cpu @27ºC => 0.706V)
    lcd.move_to(0,3)
    lcd.putstr(str(cpuTemp) + chr(223) + "C")
            #EXTERNAL SENSOR
    extTemp = (extTempSensor.read_u16())
        #VOLTAGE    
            #BUS
    busVolt = round((busVoltSensor.read_u16() * 3.3 / 65535 * 7.75),1) #read and calculate bus voltage 
    print(busVolt)
    lcd.move_to(0,0)
    lcd.putstr("BUS VOLTAGE: " + str(busVolt) + " V")
    
        #BRIGHTNESS CONTROL
    ldrValue = ldr.read_u16()#read LDR
    brightValue = int(ldrValue*100/60000)#Bright value conversion to 0-100%
    lcdLed.freq(1000) #lcd led PWM frequency
    lcdLedSetValue = brightValue #set a value from 0 - 100%
    lcdLed.duty_u16(int(65535 * lcdLedSetValue / 100)) #apply PWM pulse to LCD led
    lcd.move_to(16,3)
    lcd.putstr(str(brightValue) + "%")
    
    time.sleep(1) #time delay
    file.close()    #file close
    
    
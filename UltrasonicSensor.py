"""
__        ___    ____ _____ _____     __  __  ___  _   _ ___ _____ ___  ____  
\ \      / / \  / ___|_   _| ____|   |  \/  |/ _ \| \ | |_ _|_   _/ _ \|  _ \ 
 \ \ /\ / / _ \ \___ \ | | |  _|     | |\/| | | | |  \| || |  | || | | | |_) |
  \ V  V / ___ \ ___) || | | |___    | |  | | |_| | |\  || |  | || |_| |  _ < 
   \_/\_/_/   \_\____/ |_| |_____|___|_|  |_|\___/|_| \_|___| |_| \___/|_| \_\
                                |_____|                                       
"""

#Libraries
from signalrcore.hub_connection_builder import HubConnectionBuilder
import RPi.GPIO as GPIO
import time
import random
import threading
import sys

EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

weight = 0
fillingLevel = 0

   
def refreshData(self):
    hub_connection.send("SendData", ["%.2f" %weight, "%.2f" %fillingLevel])

server_url = "ws://waste-monitor.azurewebsites.net/wasteMonitorHub"
hub_connection = HubConnectionBuilder().with_url(server_url).build()    #Nawiazanie polaczenia
hub_connection.on("Refresh", refreshData)

def openConnection():
    hub_connection.start()
    time.sleep(10)
    
def closeConnection():
    hub_connection.stop()
 
def sendCollectedData():
    hub_connection.send("SendData", ["%.2f" %weight,"%.2f" %fillingLevel])      
    time.sleep(10)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return round(distance/100, 2)
 
if __name__ == '__main__':
    
    hx = HX711(5, 6)
    hx.set_reading_format("MSB", "MSB")
    hx.set_reference_unit(-11)
    hx.reset()
    hx.tare()
    
    try:
        openConnection()
        #counter = time.time()
        while True:
            weight =1.2*hx.get_weight(5)/10000
            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
            fillingLevel = (0.51-distance())*2
           # if counter == 
            sendCollectedData()

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        closeConnection()
        GPIO.cleanup()


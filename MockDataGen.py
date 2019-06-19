#[{"id":1,"dateTime":"2019-06-11T17:07:41.8148933","weight":20.0,"fillingLevel":0.5,"wasEmptied":false}]
from signalrcore.hub_connection_builder import HubConnectionBuilder
import numpy
import random
import threading
import sys

#PARAMETERS FOR SENDING
weight = 0
fillingLevel = 0
isEmptied = False
dateOfMeasure = "2019-05"

#CONNECTION STUFF
server_url = "ws://waste-monitor.azurewebsites.net/wasteMonitorHub"
hub_connection = HubConnectionBuilder().with_url(server_url).build()    #Nawiazanie polaczenia
hub_connection.on("Refresh", refreshData)

def openConnection():
    hub_connection.start()
    time.sleep(10)
    
def closeConnection():
    hub_connection.stop()

def sendCollectedData():
    hub_connection.send("SendData", [dateOfMeasure, "%.2f" %weight,"%.2f" %fillingLevel, isEmptied])
    time.sleep(10)

#MAIN LOOP
for i in range(1, 31):
    for j in range(1,5):
        if i < 10:
            dateOfMeasure = f"2019-05-0{i}T17:07:41.8148933"
        else:
            dateOfMeasure = f"2019-05-{i}T17:07:41.8148933"

        isEmptied = numpy.random.choice([True, False], p=[0.1, 0.9])
        sendCollectedData()
        print(dateOfMeasure + " " + str(isEmptied))

#! /usr/bin/env python

import sounddevice as sd
import time
import datetime as dt
import numpy as np
import sqlite3
import statistics
import subprocess
import sys

ALERT_TRIP_LEVEL = 4

prevVolume = 0
volumeReadings = []

def print_volume(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    global volumeReadings
    volumeReadings.append(volume_norm)
    #print(f'Microphone Volume: {volume_norm:.2f}')



dbConnection = sqlite3.connect(sys.path[0] + "/../Database/NoiseRecords.db")

dbCursor = dbConnection.cursor()
loopsSinceRec = 0

def trip_alarm():
    weekno = dt.datetime.today().weekday()
    if weekno > 4: #weekend
        return
    hour = dt.datetime.now().hour
    if hour < 5 or hour > 18: #only trigger between 5am and 6pm
        return
    
    #record alarm triggered
    global dbCursor
    dbCursor.execute("insert into alarm_history values ((julianday('now') - 2440587.5)*86400.0)")

    #execute shell script
    subprocess.call(['sh', sys.path[0] + '/../BatchFiles/TestBatch.sh'])



while True:
    volumeReadings = []
    with sd.InputStream(callback=print_volume):
        sd.sleep(1000)
    volumeAvg = statistics.median(volumeReadings)
    loopsSinceRec +=1
    #only record if big difference
    if loopsSinceRec > 30 or abs(prevVolume - volumeAvg) > 0.2 :
        if loopsSinceRec > 1:
            dbCursor.execute("insert into noise_records values ((julianday('now') - 2440587.5)*86400.0 - 1, ?);",[prevVolume])
        dbCursor.execute("insert into noise_records values ((julianday('now') - 2440587.5)*86400.0, ?);",[volumeAvg])
        if volumeAvg > ALERT_TRIP_LEVEL:
            trip_alarm()
        dbConnection.commit()
        prevVolume = volumeAvg
        loopsSinceRec = 0

    #time.sleep(1)
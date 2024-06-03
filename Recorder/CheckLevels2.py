#! /usr/bin/env python

import sounddevice as sd
import time
import datetime as dt
import numpy as np
import sqlite3
import statistics
import subprocess
import sys

ALERT_TRIP_LEVEL = 3.5

prevMean = 0
prevMedian = 0
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
    dbCursor.execute("insert into alarm_history values (?);",[time.time()])

    #execute shell script
    subprocess.call(['sh', sys.path[0] + '/../BatchFiles/FlashLight.sh'])



while True:
    volumeReadings = []
    #print("tick")
    with sd.InputStream(callback=print_volume):
        sd.sleep(1000)
    volumeMean = statistics.mean(volumeReadings)
    volumeMedian = statistics.median(volumeReadings)
    loopsSinceRec +=1
    #only record if big difference
    if loopsSinceRec > 60 or abs(prevMean - volumeMean) > 0.2 or abs(prevMedian - volumeMedian) > 0.2:
        #print("insert " + str(volumeMedian))
        if loopsSinceRec > 1:
            dbCursor.execute("insert into noise_records (record_time, noise_level_mean, noise_level_median) values (?, ?, ?);",[time.time() -0.5, prevMean, prevMedian])
        dbCursor.execute("insert into noise_records (record_time, noise_level_mean, noise_level_median) values (?, ?, ?);",[time.time(), volumeMean, volumeMedian])
        if volumeMean > ALERT_TRIP_LEVEL:
            trip_alarm()
        dbConnection.commit()
        prevMean = volumeMean
        prevMedian = volumeMedian
        loopsSinceRec = 0

    #time.sleep(1)
#! /usr/bin/env python

import sounddevice as sd
import time
import numpy as np
import sqlite3

totalReadings = 0
numReadins = 0

def print_volume(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    global numReadins, totalReadings
    numReadins +=1
    totalReadings +=volume_norm
    #print(f'Microphone Volume: {volume_norm:.2f}')

dbConnection = sqlite3.connect("/home/noisemeter/NoiseChartSite/Database/NoiseRecords.db")

dbCursor = dbConnection.cursor()

while True:
    totalReadings = 0
    numReadins = 0
    with sd.InputStream(callback=print_volume):
        sd.sleep(500)
    volume = totalReadings/numReadins
    dbCursor.execute("insert into noise_records values ((julianday('now') - 2440587.5)*86400.0, ?);",[volume])
    dbConnection.commit();
    #time.sleep(1)
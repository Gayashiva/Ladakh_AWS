#!/usr/bin/python3

import time
from datetime import datetime
import sys
import os
import csv
import serial

path = "/home/pi/AWS/Data/"
file_path = os.path.join(path, "kit.csv")

x = []
ser = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)
counter = 0
samples = 3

win_dir = 0
win_avg = 0
win_max = 0
temp = 0
hum = 0
pressure = 0


def win_direction():
    return int(x[1:4])


def windspeedaverage():
    t = 0.44704 * float(x[5:8])
    return float(t)


def windspeedmax():
    t = 0.44704 * float(x[9:12])
    return float(t)


def temperature():
    t = (float(x[13:16]) - 32.00) * 5.00 / 9.00
    return t


def humidity():  # //Humidity
    return float(x[25:27])


def barpressure():  # //Barometric Pressure
    t = float(x[28:33])
    return t / 10.00


file = open(file_path, "a")
if os.stat(file_path).st_size == 0:
    file.write(
        "Datetime,Wind_Direction,Wind_SpeedAvg,Wind_SpeedMax,Temp,Humidity,Pressure\n"
    )
x = ser.readline()
# print("Kit: ", x)

while counter < samples:
    win_dir += win_direction()
    win_avg += windspeedaverage()
    win_max += windspeedmax()
    temp += temperature()
    hum += humidity()
    pressure += barpressure()

    counter += 1
    time.sleep(0.5)

win_dir /= samples
win_avg /= samples
win_max /= samples
temp /= samples
hum /= samples
pressure /= samples
dt = datetime.now()
dt = dt.strftime("%Y-%m-%d %H:%M")
# print("wind direction: ", win_dir, " degrees")
# print("wind speed avg: ", win_avg, " m/s")
# print("wind speed: ", win_max, " m/s")
# print("temperature: ", temp, " centigrade")
# print("humidity: ", hum, "%")
# print("pressure: ", pressure, "hpa")
file.write(
    str(dt)
    + ","
    + str(win_dir)
    + ","
    + str(round(win_avg, 3))
    + ","
    + str(round(win_max, 3))
    + ","
    + str(round(temp, 2))
    + ","
    + str(round(hum, 2))
    + ","
    + str(pressure)
    + "\n"
)
file.flush()

file.close()
sys.exit()

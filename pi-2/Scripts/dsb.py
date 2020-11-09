#!/usr/bin/python3
from modules.ds18b20 import DS18B20
from time import sleep
from datetime import datetime
import sys
import os
import csv

f = open("/etc/hostname")
hostname = f.read().strip().replace(" ", "")
f.close()

path = "/home/pi/AWS/"
file_path = os.path.join(path, "Water_Temp.csv")

file = open(file_path, "a")
if os.stat(file_path).st_size == 0:
    file.write("Datetime,Water_Temp\n")

counter = 0
x = 0
Db = 0
Db1 = 0
samples = 5

while counter < samples:
    # Read temperature.
    x = DS18B20()
    count = x.device_count()
    print(count)
    # check if both the devices are working
    sleep(2)
    Db += round(x.tempC(0), 3)
    if count > 1:
        Db1 += round(x.tempC(1), 3)

    counter += 1
    sleep(1)

Db /= samples
Db1 /= samples

# Calibrate
Db = Db - 5.47

dt = datetime.now()
print("DSB", Db)
file.write(
    str(dt.strftime(dt.strftime("%Y-%m-%d %H:%M"))) + "," + str(round(Db, 2)) + "\n"
)
file.flush()

file.close()
sys.exit()

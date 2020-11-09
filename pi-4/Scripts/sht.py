#!/usr/bin/python3
# <p># Distributed with a free-will license.<br># Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SHT25
# This code is designed to work with the SHT25_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Humidity?sku=SHT25_I2CS#tabs-0-product_tabset-2</p><p>import smbus

import csv
import sys
import os
from time import sleep
from datetime import datetime

import time
import smbus  # </p><p># Get I2C bus

bus = smbus.SMBus(4)  # </p><p># SHT25 address, 0x40(64)
# Send temperature measurement command
#       0xF3(243)   NO HOLD master
counter = 0
samples = 5

path = "/home/pi/AWS/"
file_path = os.path.join(path, "air_temp.csv")

file = open(file_path, "a")
if os.stat(file_path).st_size == 0:
    file.write("Datetime,SHT_Temp,SHT_Humidity\n")


def SHT20():
    bus.write_byte(0x40, 0xF3)
    time.sleep(0.5)  # SHT25 address, 0x40(64)
    # Read data back, 2 bytes
    # Temp MSB, Temp LSB
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)  # Convert the data
    temp = data0 * 256 + data1
    cTemp = round((-46.85 + (temp * (175.72 / 65536.0))), 4)
    fTemp = cTemp * 1.8 + 32  # SHT25 address, 0x40(64)
    # Send humidity measurement command
    #       0xF5(245)   NO HOLD master
    bus.write_byte(0x40, 0xF5)
    time.sleep(0.5)  # SHT25 address, 0x40(64)
    # Read data back, 2 bytes
    # Humidity MSB, Humidity LSB
    data0 = bus.read_byte(0x40)
    data1 = bus.read_byte(0x40)  # Convert the data
    humidity = data0 * 256 + data1
    humidity = round((-6 + ((humidity * 125.0) / 65536.0)), 4)  # Output data to screen
    # print (humidity)
    return cTemp, humidity


temperature = 0
humidity = 0

while counter < samples:
    tem = SHT20()
    time.sleep(1)
    temperature = temperature + tem[0]
    humidity = humidity + tem[1]

    counter += 1
    sleep(1)

temperature /= samples
humidity /= samples

print("Temperature in Celsius is : %.2f C" % temperature)
dt = datetime.now()
file.write(
    str(dt.strftime("%Y-%m-%d %H:%M"))
    + ","
    + str(round(temperature, 3))
    + ","
    + str(round(humidity, 2))
    + "\n"
)
file.flush()

file.close()
sys.exit()

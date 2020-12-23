#!/usr/bin/python3
# Simple demo of the MAX31865 thermocouple amplifier.
# Will print the temperature every second.

from time import sleep
from datetime import datetime
import sys
import board
import busio
import digitalio
import os
import csv
import adafruit_max31865

path = "/home/pi/AWS/Data/"
file_path = os.path.join(path, "ice_temp.csv")

# Initialize SPI bus and sensor.
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D17)  # Chip select of the MAX31865 board.
sensor = adafruit_max31865.MAX31865(spi, cs, wires=4)
# Note you can optionally provide the thermocouple RTD nominal, the reference
# resistance, and the number of wires for the sensor (2 the default, 3, or 4)
# with keyword args:
# sensor = adafruit_max31865.MAX31865(spi, cs, rtd_nominal=100, ref_resistor=430.0, wires=2)
file = open(file_path, "a")
if os.stat(file_path).st_size == 0:
    file.write("Datetime,Ice_Temp\n")

counter = 0
temp = 0
samples = 5

while counter < samples:
    # Read temperature.
    temp += sensor.temperature
    counter += 1
    sleep(0.2)

temp = temp / samples

dt = datetime.now()
dt = dt.strftime("%Y-%m-%d %H:%M")
if temp > 50:
    print(dt, "Ice sensor error")
    print("Temperature in Celsius is : %.2f C" % temp)

file.write(
    str(dt) + "," + str(round(temp, 3)) + "\n"
)
file.flush()


file.close()
sys.exit()

#!/usr/bin/python3
import sys

from time import sleep
from datetime import datetime
import os
from modules.DFRobot_ADS1115 import ADS1115

ADS1115_REG_CONFIG_PGA_2_048V = 0x04  # 2.048V range = Gain 2 (default)
ads1115 = ADS1115()

path = "/home/pi/AWS/Data/"
file_path = os.path.join(path, "adc.csv")

file = open(file_path, "a")
if os.stat(file_path).st_size == 0:
    file.write("Datetime,UV,IRTemp,Water_Pressure,Water_Level\n")

counter = 0
IRTemp = 0
Water_Pressure = 0
Water_level = 0
uvLevel = 0
uvIntensity = 0
samples = 5

# //The Arduino Map function but for floats
# //From: http://forum.arduino.cc/index.php?topic=3922.0
def mapfloat(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


while counter < samples:
    # Set the IIC address
    ads1115.setAddr_ADS1115(0x48)
    # Sets the gain and input voltage range.
    ads1115.setGain(ADS1115_REG_CONFIG_PGA_2_048V)

    # Get the Digital Value of Analog of selected channel
    adc0 = ads1115.readVoltage(0)
    adc0 = float(adc0["r"] * 5 / 1024)
    adc0 = (adc0 - 1.73828125) * 400 * 10  # hPa
    # adc0 +=344.21 - 273.4375
    Water_Pressure += adc0
    sleep(0.2)

    # adc1 = ads1115.readVoltage(1)
    # adc1 = float((adc1["r"] / 120) - 4)
    # adc1 = float(adc1 * 312.5)  # mm
    # adc1 += 285 - 257.812
    # Water_level += adc1
    # sleep(0.2)

    adc2 = ads1115.readVoltage(2)
    adc2 = float(adc2["r"] / 1024)
    IRTemp = IRTemp + float(adc2 / 3 * 450 - 70)
    sleep(0.2)

    adc3 = ads1115.readVoltage(3)
    uvLevel += float(adc3["r"])
    outputVoltage = 5.0 * float(adc3["r"]) / 1024
    uvIntensity += (
        mapfloat(outputVoltage, 0.99, 2.9, 0.0, 15.0) / 1000 * 100 * 100
    )  # W/m2

    counter += 1
    sleep(1)

dt = datetime.now()
dt = dt.strftime("%Y-%m-%d %H:%M")
IRTemp /= samples
Water_Pressure /= samples
Water_level /= samples
uvLevel /= samples
uvIntensity /= samples

if Water_Pressure == 33098.116:
    print(dt, "Pressure sensor error")
if IRTemp > 10:
    print(dt, "Infrared sensor error")
# print("ADC", uvIntensity, IRTemp, Water_Pressure)

file.write(
    str(dt)
    + ","
    + str(round(uvIntensity, 3))
    + ","
    + str(round(IRTemp, 3))
    + ","
    + str(round(Water_Pressure, 3))
    + ","
    + str(round(Water_level, 3))
    + "\n"
)
file.flush()
file.close()
sys.exit()

#!/usr/bin/python3
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

f = open("/etc/hostname")
hostname = f.read().strip().replace(" ", "")
f.close()

path = "/home/pi/AWS/Data/"
# path = "/home/surya/AWS/pi-0/Data/"
file_path = os.path.join(path[:-5], hostname + "_outputs.pdf")

df_adc = pd.read_csv(path + "adc.csv", sep=",", header=0, parse_dates=["Datetime"])

df_PT100 = pd.read_csv(
    path + "ice_temp.csv", sep=",", header=0, parse_dates=["Datetime"]
)

# df_SHT = pd.read_csv(
#     path + "air_temp.csv", sep=",", header=0, parse_dates=["Datetime"]
# )

df_DSB = pd.read_csv(
    path + "water_temp.csv", sep=",", header=0, parse_dates=["Datetime"]
)

df_kit = pd.read_csv(path + "kit.csv", sep=",", header=0, parse_dates=["Datetime"])

print(df_kit.Datetime.iloc[-1])

pp = PdfPages(file_path)

fig, (ax1, ax2, ax3) = plt.subplots(
    nrows=3, ncols=1, sharex="col", sharey="row", figsize=(16, 14)
)
x = df_adc.Datetime

y1 = df_adc.UV
ax1.plot(x, y1, "k-", linewidth=0.5)
ax1.set_ylabel("UV Intensity [$W\\,m^{-2}$]")
ax1.grid()

y2 = df_adc.IRTemp
ax2.plot(x, y2, "k-", linewidth=0.5)
ax2.set_ylabel("IR Temperature [$\\degree C$]")
ax2.grid()

y1 = df_adc.Water_Pressure
ax3.plot(x, y1, "k-", linewidth=0.5)
ax3.set_ylabel("Fountain Pressure [$hPa$]")
ax3.grid()

ax3t = ax3.twinx()
ax3t.plot(x, df_adc.Water_Level / 1000, "b-", linewidth=0.5)
ax3t.set_ylabel("Water height [$m$]", color="b")
for tl in ax3t.get_yticklabels():
    tl.set_color("b")
ax1.xaxis.set_major_locator(mdates.DayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax1.xaxis.set_minor_locator(mdates.HourLocator())

fig.autofmt_xdate()
pp.savefig(bbox_inches="tight")
plt.clf()

fig, (ax1, ax2, ax3) = plt.subplots(
    nrows=3, ncols=1, sharex="col", sharey="row", figsize=(16, 14)
)
x = df_kit.Datetime

y1 = df_kit.Wind_SpeedAvg
ax1.plot(x, y1, "k-", linewidth=0.5)
ax1.set_ylabel("Wind_SpeedAvg [$m\\,s^{-1}$]")
ax1.grid()

y2 = df_kit.Temp
ax2.plot(x, y2, "k-", linewidth=0.5)
ax2.set_ylabel("Temperature [$\\degree C$]")
ax2.grid()

y1 = df_kit.Pressure
ax3.plot(x, y1, "k-", linewidth=0.5)
ax3.set_ylabel("Air Pressure [$mbar$]")
ax3.grid()

ax3t = ax3.twinx()
ax3t.plot(x, df_kit.Humidity, "b-", linewidth=0.5)
ax3t.set_ylabel("Humidity", color="b")
for tl in ax3t.get_yticklabels():
    tl.set_color("b")
ax1.xaxis.set_major_locator(mdates.DayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax1.xaxis.set_minor_locator(mdates.HourLocator())

fig.autofmt_xdate()
pp.savefig(bbox_inches="tight")
plt.clf()

ax1 = fig.add_subplot(111)
x = df_PT100.Datetime
y1 = df_PT100.Ice_Temp
ax1.plot(x, y1, "k-", linewidth=0.5)
ax1.set_ylabel("Ice_Temperature [$\\degree C$]")
ax1.grid()
ax1.xaxis.set_major_locator(mdates.DayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax1.xaxis.set_minor_locator(mdates.HourLocator())

fig.autofmt_xdate()
pp.savefig(bbox_inches="tight")
plt.clf()

# ax1 = fig.add_subplot(111)
# x = df_SHT.Datetime
# y1 = df_SHT.SHT_Temp
# ax1.plot(x, y1, "k-", linewidth=0.5)
# ax1.set_ylabel("Temperature [$\\degree C$]")
# ax1.grid()

# ax1t = ax1.twinx()
# ax1t.plot(x, df_SHT.SHT_Humidity, "b-", linewidth=0.5)
# ax1t.set_ylabel("Humidity", color="b")
# for tl in ax1t.get_yticklabels():
#    tl.set_color("b")

# ax1.xaxis.set_major_locator(mdates.DayLocator())
# ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
# ax1.xaxis.set_minor_locator(mdates.HourLocator())

# fig.autofmt_xdate()
# pp.savefig(bbox_inches="tight")
# plt.clf()

ax1 = fig.add_subplot(111)
x = df_DSB.Datetime
y1 = df_DSB.Water_Temp
ax1.plot(x, y1, "k-", linewidth=0.5)
ax1.set_ylabel("Water Temperature [$\\degree C$]")
ax1.grid()

ax1.xaxis.set_major_locator(mdates.DayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax1.xaxis.set_minor_locator(mdates.HourLocator())

fig.autofmt_xdate()
pp.savefig(bbox_inches="tight")
plt.clf()

pp.close()

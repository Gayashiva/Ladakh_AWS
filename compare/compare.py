import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
from pandas.plotting import register_matplotlib_converters
import os
from windrose import WindroseAxes

DIRNAME = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

site = "Gangles"
path = os.path.join(DIRNAME, "pi-2/")
path_AWS = os.path.join(DIRNAME, site + "_AWS/")

df_SHT = pd.read_csv(path + "Air_Temp.csv", sep=",", header=0, parse_dates=["Datetime"])
df_SHT = df_SHT.set_index("Datetime").resample("15T").mean().reset_index()

start = datetime(2020, 10, 15, 15, 15)
end = df_SHT["Datetime"].iloc[-1]

mask = (df_SHT["Datetime"] >= start) & (df_SHT["Datetime"] <= end)
df_SHT = df_SHT[mask]

df_DSB = pd.read_csv(
    path + "Water_Temp.csv", sep=",", header=0, parse_dates=["Datetime"]
)
df_DSB = df_DSB.set_index("Datetime").resample("15T").mean().reset_index()
mask = (df_DSB["Datetime"] >= start) & (df_DSB["Datetime"] <= end)
df_DSB = df_DSB[mask]

df_PT = pd.read_csv(path + "Ice_Temp.csv", sep=",", header=0, parse_dates=["Datetime"])
df_PT = df_PT.set_index("Datetime").resample("15T").mean().reset_index()
mask = (df_PT["Datetime"] >= start) & (df_PT["Datetime"] <= end)
df_PT = df_PT[mask]

df_kit = pd.read_csv(path + "Kit.csv", sep=",", header=0, parse_dates=["Datetime"])
df_kit = df_kit.set_index("Datetime").resample("15T").mean().reset_index()
mask = (df_kit["Datetime"] >= start) & (df_kit["Datetime"] <= end)
df_kit = df_kit[mask]

df_AWS = pd.read_csv(
    path_AWS + site + "_Table15min.dat", skiprows=1, header=0, parse_dates=["TIMESTAMP"]
)
df_AWS = df_AWS[2:]
df_AWS["TIMESTAMP"] = pd.to_datetime(df_AWS["TIMESTAMP"])

mask = (df_AWS["TIMESTAMP"] >= start) & (df_AWS["TIMESTAMP"] <= end)
df_AWS = df_AWS[mask]
df_AWS = df_AWS[["TIMESTAMP", "AirTC_Avg", "RH", "WS", "WindDir"]]

df_AWS2 = pd.read_csv(
    path_AWS + site + "_Table60Min.dat", skiprows=1, header=0, parse_dates=["TIMESTAMP"]
)
df_AWS2 = df_AWS2[2:]
df_AWS2["TIMESTAMP"] = pd.to_datetime(df_AWS2["TIMESTAMP"])

mask = (df_AWS2["TIMESTAMP"] >= start) & (df_AWS2["TIMESTAMP"] <= end)
df_AWS2 = df_AWS2[mask]

days = pd.date_range(start=start, end=end, freq="15T")

df_out = pd.DataFrame({"When": days})
df_out = df_out.set_index("When")
df_AWS = df_AWS.set_index("TIMESTAMP")
df_AWS2 = df_AWS2.set_index("TIMESTAMP")
df_SHT = df_SHT.set_index("Datetime")
df_DSB = df_DSB.set_index("Datetime")
df_PT = df_PT.set_index("Datetime")
df_kit = df_kit.set_index("Datetime")

df_out["T_AWS"] = df_AWS["AirTC_Avg"].astype(float)
df_out["RH_AWS"] = df_AWS["RH"].astype(float)
df_out["WindDir_AWS"] = df_AWS["WindDir"].astype(float)
df_out["P_AWS"] = df_AWS2["BP_mbar"].astype(float)
print(df_out.tail())
df_out["T_Pi"] = df_SHT["SHT_Temp"]
df_out["Water_Temp"] = df_DSB["Water_Temp"]
df_out["Ice_Temp"] = df_PT["Ice_Temp"]
df_out["RH_Pi"] = df_SHT["SHT_Humidity"]
df_out["v_AWS"] = df_AWS["WS"].astype(float)
df_out["v_Pi"] = df_kit["Wind_SpeedAvg"]
df_out["P_Pi"] = df_kit["Pressure"]
df_out["WindDir_Pi"] = df_kit["Wind_Direction"]

df_out = df_out.reset_index()

RMSE_T = ((df_out.T_AWS - df_out.T_Pi) ** 2).mean() ** 0.5
RMSE_T2 = ((df_out.T_AWS - df_out.Water_Temp) ** 2).mean() ** 0.5
RMSE_v = ((df_out.v_AWS - df_out.v_Pi) ** 2).mean() ** 0.5
RMSE_RH = ((df_out.RH_AWS - df_out.RH_Pi) ** 2).mean() ** 0.5
RMSE_P = ((df_out.P_AWS - df_out.P_Pi) ** 2).mean() ** 0.5
# df_out.v_Pi = df_out.v_Pi + RMSE_v
# df_out.RH_Pi = df_out.RH_Pi + RMSE_RH
# df_out.P_Pi = df_out.P_Pi + RMSE_P
# df_out.Water_Temp= df_out.Water_Temp+ RMSE_T2

pp = PdfPages("compare/compare" + ".pdf")
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.scatter(df_out.T_AWS, df_out.T_Pi, s=2)
ax1.set_xlabel("AWS Temp")
ax1.set_ylabel("Pi Temp")
ax1.grid()
lims = [
    np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
    np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
]
# now plot both limits against eachother
ax1.plot(lims, lims, "--k", alpha=0.25, zorder=0)
ax1.set_aspect("equal")
ax1.set_xlim(lims)
ax1.set_ylim(lims)
pp.savefig(bbox_inches="tight")
plt.clf()

ax1 = fig.add_subplot(111)
ax1.scatter(df_out.T_AWS, df_out.Water_Temp, s=2)
ax1.set_xlabel("AWS Temp")
ax1.set_ylabel("Pi Water Temp")
ax1.grid()
lims = [
    np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
    np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
]
# now plot both limits against eachother
ax1.plot(lims, lims, "--k", alpha=0.25, zorder=0)
ax1.set_aspect("equal")
ax1.set_xlim(lims)
ax1.set_ylim(lims)
pp.savefig(bbox_inches="tight")
plt.clf()

ax1 = fig.add_subplot(111)
ax1.scatter(df_out.T_AWS, df_out.Ice_Temp, s=2)
ax1.set_xlabel("AWS Temp")
ax1.set_ylabel("Pi Ice Temp")
ax1.grid()
lims = [np.min([-25, -25]), np.max([25, 25])]  # min of both axes  # max of both axes
# now plot both limits against eachother
ax1.plot(lims, lims, "--k", alpha=0.25, zorder=0)
ax1.set_aspect("equal")
ax1.set_xlim(lims)
ax1.set_ylim(lims)
pp.savefig(bbox_inches="tight")
plt.clf()

ax1 = fig.add_subplot(111)
ax1.scatter(df_out.RH_AWS, df_out.RH_Pi, s=2)
ax1.set_xlabel("AWS RH")
ax1.set_ylabel("Pi RH")
ax1.grid()
lims = [
    np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
    np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
]
# now plot both limits against eachother
ax1.plot(lims, lims, "--k", alpha=0.25, zorder=0)
ax1.set_aspect("equal")
ax1.set_xlim(lims)
ax1.set_ylim(lims)
pp.savefig(bbox_inches="tight")
plt.clf()

ax1 = fig.add_subplot(111)
ax1.scatter(df_out.v_AWS, df_out.v_Pi, s=2)
ax1.set_xlabel("AWS Wind")
ax1.set_ylabel("Pi Wind")
ax1.grid()
lims = [
    np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
    np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
]
# now plot both limits against eachother
ax1.plot(lims, lims, "--k", alpha=0.25, zorder=0)
ax1.set_aspect("equal")
ax1.set_xlim(lims)
ax1.set_ylim(lims)
pp.savefig(bbox_inches="tight")
plt.clf()

ax1 = fig.add_subplot(111)
ax1.scatter(df_out.P_AWS, df_out.P_Pi, s=2)
ax1.set_xlabel("AWS P")
ax1.set_ylabel("Pi P")
ax1.grid()
lims = [
    np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
    np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
]
# now plot both limits against eachother
ax1.plot(lims, lims, "--k", alpha=0.25, zorder=0)
ax1.set_aspect("equal")
ax1.set_xlim(lims)
ax1.set_ylim(lims)
pp.savefig(bbox_inches="tight")
plt.clf()

ax1 = fig.add_subplot(111)
ax1.scatter(df_out.WindDir_AWS, df_out.WindDir_Pi, s=2)
ax1.set_xlabel("AWS Dir")
ax1.set_ylabel("Pi Dir")
ax1.grid()
lims = [
    np.min([ax1.get_xlim(), ax1.get_ylim()]),  # min of both axes
    np.max([ax1.get_xlim(), ax1.get_ylim()]),  # max of both axes
]
# now plot both limits against eachother
ax1.plot(lims, lims, "--k", alpha=0.25, zorder=0)
ax1.set_aspect("equal")
ax1.set_xlim(lims)
ax1.set_ylim(lims)
pp.savefig(bbox_inches="tight")
plt.clf()
theta = df_out["WindDir_AWS"]
speed = df_out["v_AWS"]
ax = WindroseAxes.from_ax()
ax.bar(theta, speed)
ax.legend()
pp.savefig(bbox_inches="tight")
plt.clf()

theta = df_out["WindDir_Pi"]
speed = df_out["v_Pi"]
ax = WindroseAxes.from_ax()
ax.bar(theta, speed)
ax.legend()
pp.savefig(bbox_inches="tight")
plt.clf()
pp.close()


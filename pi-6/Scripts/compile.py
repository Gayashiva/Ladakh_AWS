#!/usr/bin/python3
import os
import glob
import pandas as pd
import re
import datetime as dt

path = "/home/pi/AWS/Data/"
# path = "/home/surya/AWS/pi-0/Data/"
file_path = os.path.join(path[:-5], "gangles.csv")

os.chdir(path)

extension = "csv"
all_filenames = [i for i in glob.glob("*.{}".format(extension))]

df = pd.concat(
    [
        pd.read_csv(f, parse_dates=["Datetime"]).set_index("Datetime")
        for f in all_filenames
    ]
)
df.index = df.index.strftime("%Y-%m-%d %H:%M")
df = df.sort_index()
df = df.drop(["Water_Level", "Temp", "Humidity"], axis=1)
df = df.groupby(df.index).sum()
df = df.round(2)
df.to_csv(file_path)

import os
import glob
import pandas as pd
import re
import datetime as dt

# set working directory
os.chdir("/home/surya/AWS/Hobo")

# find all csv files in the folder
# use glob pattern matching -> extension = 'csv'
# save result in list -> all_filenames
extension = "csv"
all_filenames = [i for i in glob.glob("*.{}".format(extension))]

reobj = re.compile("\Aphaterak_hobo")
file = [f for f in all_filenames if reobj.match(f)][0]
hobo = pd.read_csv(file)
hobo = hobo.drop(hobo.columns[3], axis=1)
hobo.columns = ["Datetime", "air_temp", "RH"]
hobo["Datetime"] = pd.to_datetime(hobo["Datetime"], format="%y-%m-%d %H:%M:%S")
hobo["Datetime"] = hobo["Datetime"].dt.strftime("%Y-%m-%d %H:%M")
print(hobo.tail())

# set working directory
os.chdir("/home/surya/AWS/pi-0")
hobo.to_csv("hobo.csv", index=False)

extension = "csv"
all_filenames = [i for i in glob.glob("*.{}".format(extension))]
print(all_filenames)

df = pd.concat([pd.read_csv(f) for f in all_filenames])
df["Datetime"] = pd.to_datetime(df["Datetime"], format="%Y-%m-%d %H:%M")
df.head()
df.to_csv("combined_csv.csv", index=False, encoding="utf-8-sig")

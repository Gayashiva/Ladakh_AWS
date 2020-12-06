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
hobo.columns = ["Datetime", "Air_Temp", "RH"]
hobo["Datetime"] = pd.to_datetime(hobo["Datetime"], format="%y-%m-%d %H:%M:%S")
hobo["Datetime"] = hobo["Datetime"].dt.strftime("%Y-%m-%d %H:%M")

hobo.to_csv("/home/surya/AWS/pi-0/Data/hobo.csv", index=False)

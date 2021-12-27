import pymongo
import csv
from pymongo import MongoClient
import pandas as pd
import numpy as np

cluster = MongoClient(
    "mongodb+srv://andrew:1234@cluster0.pgi1d.mongodb.net/CalgaryTraffic?ssl=true&ssl_cert_reqs=CERT_NONE")
db = cluster["Test"]

# DATABASE COLLECTION REMOVAL
# db.trafficVolume2018.delete_many({})
# db.Accident2016.delete_many({})
# db.Accident2017.delete_many({})
# db.Accident2018.delete_many({})
# db.TrafficVolume2016.delete_many({})
# db.TrafficVolume2017.delete_many({})
# db.TrafficVolume2018.delete_many({})

# Load Traffic Volume Data
df_volume_2016 = pd.read_csv("CSV/TrafficFlow2016_OpenData.csv")
df_volume_2017 = pd.read_csv("CSV/2017_Traffic_Volume_Flow.csv")
df_volume_2018 = pd.read_csv("CSV/Traffic_Volumes_for_2018.csv")

# Convert to dictionary format for database upload
df_volume_2016.reset_index(inplace = True)
df_volume_2017.reset_index(inplace = True)
df_volume_2018.reset_index(inplace = True)

dict_volume_2016 = df_volume_2016.to_dict("records")
dict_volume_2017 = df_volume_2017.to_dict("records")
dict_volume_2018 = df_volume_2018.to_dict("records")

# Upload to database
db.TrafficVolume2016.insert_many(dict_volume_2016)
db.TrafficVolume2017.insert_many(dict_volume_2017)
db.TrafficVolume2018.insert_many(dict_volume_2018)

# Load Accident Data
df_incidents = pd.read_csv("CSV/Traffic_Incidents.csv")
df_incidents['START_DT'] = pd.to_datetime(df_incidents['START_DT'])

# Split data into separate years
accident_2016 = df_incidents.loc[df_incidents["START_DT"].dt.year == 2016, :]
accident_2017 = df_incidents.loc[df_incidents["START_DT"].dt.year == 2017, :]
accident_2018 = df_incidents.loc[df_incidents["START_DT"].dt.year == 2018, :]

# Convert to dictionary format for database upload
accident_2016.reset_index(inplace = True)
dict_accident_2016 = accident_2016.to_dict("records")

accident_2017.reset_index(inplace = True)
dict_accident_2017 = accident_2017.to_dict("records")

accident_2018.reset_index(inplace = True)
dict_accident_2018 = accident_2018.to_dict("records")

# Upload to database
db.Accident2016.insert_many(dict_accident_2016)
db.Accident2017.insert_many(dict_accident_2017)
db.Accident2018.insert_many(dict_accident_2018)




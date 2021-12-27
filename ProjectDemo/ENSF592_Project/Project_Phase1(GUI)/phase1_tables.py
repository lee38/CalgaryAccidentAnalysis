import pymongo
import csv
from pymongo import MongoClient
import pandas as pd
import pprint
import dns
import datetime
import string


def get_year_and_type():
    '''gets the year and type selection from the combo boxes
    '''
    year = com_box_year.get()
    type = com_box_type.get()
    print(type, year)
    return type, year


def display_table(type, year):
    '''reads combo box selection and displays table
    '''
    # type = get_year_and_type()[0]
    # year = int(get_year_and_type()[1])

    cluster = MongoClient(
        "mongodb+srv://andrew:1234@cluster0.pgi1d.mongodb.net/CalgaryTraffic?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = cluster["Test"]

    # Determine correct database-->collection

    column_filter = {'_id': 0}
    column_sort = {'secname': 1, 'volume': 1, '_id': 0}

    table_read = 0
    table_sort = 0
    limit_count = 10

    if type == "Traffic Volume":
        if year == 2016:
            collection = db.get_collection("TrafficVolume2016")

            # Read Button Table - Alphabetical
            table_read = collection.find({}, column_filter).sort("segment_name", 1).limit(limit_count)

            # Sort Button Table - Volume Descending
            table_sort = collection.find({}, column_filter).sort("volume", -1).limit(limit_count)

        elif year == 2017:
            collection = db.get_collection("TrafficVolume2017")
            # Read Button Table - Alphabetical
            table_read = collection.find({}, column_filter).sort("index", 1).limit(limit_count)

            # Sort Button Table - Volume Descending
            table_sort = collection.find({}, column_filter).sort("volume", -1).limit(limit_count)

        elif year == 2018:
            collection = db.get_collection("TrafficVolume2018")
            # Read Button Table - Alphabetical
            table_read = collection.find({}, column_filter).sort("index", 1).limit(limit_count)

            # Sort Button Table - Volume Descending
            table_sort = collection.find({}, column_filter).sort("VOLUME", -1).limit(limit_count)

    if type == "Accident":  # NEED TO FIX THIS TO DISPLAY GRID COUNTS
        if year == 2016:
            collection = db.get_collection("Accident2016")
            table_read = collection.find({}, {'_id': 0, 'index': 0}).sort("INCIDENT INFO", 1).limit(limit_count)
            table_sort = collection.find({}, {'_id': 0, 'index': 0}).sort("Count", -1).limit(limit_count)

        elif year == 2017:
            collection = db.get_collection("Accident2017")
            table_read = collection.find({}, {'_id': 0, 'index': 0}).sort("INCIDENT INFO", 1).limit(limit_count)
            table_sort = collection.find({}, {'_id': 0, 'index': 0}).sort("Count", -1).limit(limit_count)

        elif year == 2018:
            collection = db.get_collection("Accident2018")
            table_read = collection.find({}, {'_id': 0, 'index': 0}).sort("INCIDENT INFO", 1).limit(limit_count)
            table_sort = collection.find({}, {'_id': 0, 'index': 0}).sort("Count", -1).limit(limit_count)

    return table_read, table_sort


def chart_data(type, year):
    cluster = MongoClient(
        "mongodb+srv://andrew:1234@cluster0.pgi1d.mongodb.net/CalgaryTraffic?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = cluster["Test"]

# TRAFFIC MAX
    if type == "Traffic Volume":
        if year == 2016:
            collection = db.get_collection("TrafficVolume2016")
            max = collection.find({}, {'_id': 0, 'volume': 1}).sort("volume", -1).limit(1)
            res = []
            res.append(max[0]['volume'])

        elif year == 2017:
            collection = db.get_collection("TrafficVolume2017")
            max = collection.find({}, {'_id': 0, 'volume': 1}).sort("volume", -1).limit(1)
            res = []
            res.append(max[0]['volume'])

        elif year == 2018:
            collection = db.get_collection("TrafficVolume2018")
            max = collection.find({}, {'_id': 0, 'VOLUME': 1}).sort("VOLUME", -1).limit(1)
            res = []
            res.append(max[0]['VOLUME'])

# ACCIDENT MAX
    if type == "Accident":
        if year == 2016:
            collection = db.get_collection("Accident2016")
            max = list(collection.find({}, {'_id': 0, 'Longitude' : 1, 'Latitude' : 1}).sort('Latitude', 1))
            res = []
            for i in range(len(max)):
                res.append(tuple([max[i]['Longitude'], max[i]['Latitude']]))

        elif year == 2017:
            collection = db.get_collection("Accident2017")
            max = list(collection.find({}, {'_id': 0, 'Longitude' : 1, 'Latitude' : 1}).sort('Latitude', 1))
            res = []
            for i in range(len(max)):
                res.append(tuple([max[i]['Longitude'], max[i]['Latitude']]))

        elif year == 2018:
            collection = db.get_collection("Accident2018")
            max = list(collection.find({}, {'_id': 0, 'Longitude' : 1, 'Latitude' : 1}).sort('Latitude', 1))
            res = []
            for i in range(len(max)):
                res.append(tuple([max[i]['Longitude'], max[i]['Latitude']]))

    return res


def map_data(type, year):
    cluster = MongoClient(
        "mongodb+srv://andrew:1234@cluster0.pgi1d.mongodb.net/CalgaryTraffic?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = cluster["Test"]

# TRAFFIC MAX
    if type == "Traffic Volume":
        if year == 2016:
            collection = db.get_collection("TrafficVolume2016")
            max = list(collection.find({}, {'_id': 0, 'the_geom': 1}).sort("volume", -1).limit(1))
            res = []
            tmp = []

            s = max[0]['the_geom']
            s = s.replace("MULTILINESTRING ((", '')
            tmp = s.split(",")
            s = tmp[0]
            res = s.split()
            res[0], res[1] = float(res[0]), float(res[1])

        elif year == 2017:
            collection = db.get_collection("TrafficVolume2017")
            max = list(collection.find({}, {'_id': 0, 'the_geom': 1}).sort("volume", -1).limit(1))
            res = []
            tmp = []

            s = max[0]['the_geom']
            s = s.replace("MULTILINESTRING ((", '')
            tmp = s.split(",")
            s = tmp[0]
            res = s.split()
            res[0], res[1] = float(res[0]), float(res[1])

        elif year == 2018:
            collection = db.get_collection("TrafficVolume2018")
            max = list(collection.find({}, {'_id': 0}).sort("VOLUME", -1).limit(1))
            res = []
            tmp = []

            s = max[0]['multilinestring']
            s = s.replace("MULTILINESTRING ((", '')
            tmp = s.split(",")
            s = tmp[0]
            res = s.split()
            res[0], res[1] = float(res[0]), float(res[1])

# ACCIDENT MAX
    if type == "Accident":
        if year == 2016:
            collection = db.get_collection("Accident2016")
            max = list(collection.find({}, {'_id': 0, 'Longitude' : 1, 'Latitude' : 1}).sort('Latitude', 1))
            res = []
            for i in range(len(max)):
                res.append(tuple([max[i]['Longitude'], max[i]['Latitude']]))

        elif year == 2017:
            collection = db.get_collection("Accident2017")
            max = list(collection.find({}, {'_id': 0, 'Longitude' : 1, 'Latitude' : 1}).sort('Latitude', 1))
            res = []
            for i in range(len(max)):
                res.append(tuple([max[i]['Longitude'], max[i]['Latitude']]))

        elif year == 2018:
            collection = db.get_collection("Accident2018")
            max = list(collection.find({}, {'_id': 0, 'Longitude' : 1, 'Latitude' : 1}).sort('Latitude', 1))
            res = []
            for i in range(len(max)):
                res.append(tuple([max[i]['Longitude'], max[i]['Latitude']]))

    return res


# TEST CODE FOR chart_data() and map_data()
# data = map_data("Accident", 2016)
# print(data)
# TEST CODE FOR display_table()
# table_read, table_sort = display_table("Accident", 2016)
#
# table_read = list(table_read)
# table_sort = list(table_sort)
#
# for item in table_read:
#     print(item)
#
# print("\n")
#
# for item in table_sort:
#     print(item)

import pymongo
import csv
from pymongo import MongoClient
import pandas as pd
import pprint
import dns
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import folium
from matplotlib.ticker import MaxNLocator
"""
ENSF 592 Project Phase
By David Laditan, Andrew Lee, Brandon Low-On 

The purpose of this Python script is create a GUI that will read from a databased created out of CSV files provided by the City of Calgary about traffic and accident data collected in 2016, 2017 and 2018. As the user you will be able
    -> read the data from the database
    -> sort the data by highest volume or accident count for that year
    -> compare and analyze the years
    -> create a map showcasing the area with the highest volume/traffic
"""
"""
David's Section
"""
def get_year_and_type():
    '''gets the year and type selection from the combo boxes
    '''
    year = com_box_year.get()
    type = com_box_type.get()
    print(type, year)
    return type, year

def read_database(type, year):
    '''reads data from database depending on the type and year selected by the user. Returns two versions of a table, an unsorted version and a sorted version. 

    returns: a tuple of two lists containing table rows.
            table_rows - unsorted table rows
            table_rows_sorted - sorted table rows
    '''
    cluster = MongoClient(
            "mongodb+srv://andrew:1234@cluster0.pgi1d.mongodb.net/CalgaryTraffic?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = cluster["Test"]

    # Determine correct database-->collection

    column_filter = {'_id': 0}
    column_sort = {'secname': 1, 'volume': 1, '_id': 0}

    table_read = 0
    table_sort = 0
    limit_count = 20

    if type == "Traffic Volume":
        if year == 2016:
            collection = db.get_collection("TrafficVolume2016")

            # Read Button Table - Alphabetical
            table_read = collection.find({}, column_filter).sort("segment_name", 1).limit(0)
            table_rows = [row for row in table_read]


            # Sort Button Table - Volume Descending
            table_sort = collection.find({}, column_filter).sort("volume", -1).limit(0)
            table_rows_sorted = [row for row in table_sort]


        elif year == 2017:
                collection = db.get_collection("TrafficVolume2017")
                # Read Button Table - Alphabetical
                table_read = collection.find({}, column_filter).sort("segment_name", 1).limit(0)
                table_rows = [row for row in table_read]


                # Sort Button Table - Volume Descending
                table_sort = collection.find({}, column_filter).sort("volume", -1).limit(0)
                table_rows_sorted = [row for row in table_sort]


        elif year == 2018:
                collection = db.get_collection("TrafficVolume2018")
                # Read Button Table - Alphabetical
                table_read = collection.find({}, column_filter).sort("SECNAME", 1).limit(0)
                table_rows = [row for row in table_read]


                # Sort Button Table - Volume Descending
                table_sort = collection.find({}, column_filter).sort("volume", -1).limit(0)
                table_rows_sorted = [row for row in table_sort]


    if type == "Accident":
        if year == 2016:
            collection = db.get_collection("Accident2016")
            table_read = collection.find({}, {'_id': 0, 'index': 0}).sort("INCIDENT INFO", 1).limit(0)
            table_rows = [row for row in table_read]

            table_sort = collection.find({}, {'_id': 0, 'index': 0}).sort("Count", -1).limit(0)
            table_rows_sorted = [row for row in table_sort]


        elif year == 2017:
            collection = db.get_collection("Accident2017")
            table_read = collection.find({}, {'_id': 0, 'index': 0}).sort("INCIDENT INFO", 1).limit(0)
            table_rows = [row for row in table_read]

            table_sort = collection.find({}, {'_id': 0, 'index': 0}).sort("Count", -1).limit(0)
            table_rows_sorted = [row for row in table_sort]


        elif year == 2018:
            collection = db.get_collection("Accident2018")
            table_read = collection.find({}, {'_id': 0, 'index': 0}).sort("INCIDENT INFO", 1).limit(0)
            table_rows = [row for row in table_read]

            table_sort = collection.find({}, {'_id': 0, 'index': 0}).sort("Count", -1).limit(0)
            table_rows_sorted = [row for row in table_sort]


    return table_rows, table_rows_sorted

def display_table():
    '''reads combo box selection and displays table on the GUI
    '''
    
    try:
        type = get_year_and_type()[0]
        year = int(get_year_and_type()[1])

        data = read_database(type, year)[0]
        print(data)

        create_table(data)
        display_status_message(year, type, button= "Read", is_success = True)

    except :
        display_status_message(year, type, button= "Read", is_success = False)

def display_sorted_table():
    '''Dispalys a sorted version of a specified table on the GUI
    '''
    try:
        type = get_year_and_type()[0]
        year = int(get_year_and_type()[1])

        if type == "Traffic Volume":
            data = read_database(type, year)[1]
            print(data)

        if type == "Accident":
            data = createGridDict(year, type)


        create_table(data)
        display_status_message(year, type, button= "Sort", is_success = True)

    except:
        display_status_message(year, type, button= "Sort", is_success = False)

def display_status_message(year, type, button, is_success):
    '''Displays status message for each button clicked in the GUI

        year: user selection from year combo-box
        type: user selection from type combo-box
        button: button text which identifies button e.g "Read", "Sort". string
        is_success: boolean 
    '''

    if button == "Read":
        if is_success:
            message = f"Successfully displayed {type} table for year {year}"
        else:
            message = f"Failed to display {type} table for year {year}"
    elif button == "Sort":
        if is_success:
            message = f"Successfully sorted {type} table for year {year}"          
        else:
            message = f"Failed to sort {type} table for year {year}"
    elif button == "Analysis":
        if is_success:
            message = f"Successfully displayed {type} analysis plot for year {year}"          
        else:
            message = f"Failed to display {type} analysis plot for year {year}"
    elif button == "Map":
         if is_success:
            message = f"Sucessfully displayed map of maximum {type} for year {year}"
         else:
            message = f"Failed to display map of maximum {type} for year {year}"

    lbl_status_display["text"] = message
    # if is_success == False:
    #     lbl_status_display["bg"] = "red"

def create_table(data):
    '''Creates a table 
    '''
    headings = [column_name for column_name, value in data[0].items()]

    # create and add tree (table) to frame
    tree = ttk.Treeview(frm_display, columns = headings, height = 20, show = "headings")
    tree.grid(row = 0, column = 0, sticky = "nsew")

    # configure tree (table) heading and column display
    for i in range(len(headings)):
        tree.heading(i, text = headings[i], anchor = 'w')
        tree.column(i, anchor = "w", width = 200)

    # add data rows to table  
    for row in data:
        tree.insert('', 'end', values = [value for column_name, value in row.items()])

    # scroll bars
    scroll_y = ttk.Scrollbar(frm_display, orient="vertical", command=tree.yview)
    scroll_y.grid(row =0, column =1, sticky = "ns")

    scroll_x = ttk.Scrollbar(frm_display, orient="horizontal", command= tree.xview)
    scroll_x.grid(row = 1, column = 0, sticky = "ew")

    tree.configure(yscroll = scroll_y.set, xscroll = scroll_x.set)

def display_chart():
    '''reads combo box selection and displays chart
    '''
    try:
        # get type and year from combo box 
        type = get_year_and_type()[0]
        year = get_year_and_type()[1]

        # create figure
        figure1 = plt.Figure(figsize=(5,5), dpi=70)
        ax = figure1.add_subplot(111)

        # add figure to frame
        canvas = FigureCanvasTkAgg(figure1, frm_display)
        canvas.get_tk_widget().grid(row =0, column = 0, sticky = "nsew")

        
        x = [2016, 2017, 2018]
        y = [chart_data(type, year)[0] for year in x] #get the maximum traffic volume for each year in x
        # print(y)

        if type == "Traffic Volume":
            label = "Maximum Traffic Volume"
            title = "Maximum Traffic Volume vs Year"
            y_label = "Traffic Volume"

        if type == "Accident":
            label = "Maximum Number of Accidents"
            title = "Maximum Accidents vs Year"
            y_label = "Incidents"

        

        ax.plot(x, y, marker ='*', label = label)
        ax.legend()
        ax.set_title(title)
        ax.set_xlabel('Year')
        ax.set_ylabel(y_label)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        display_status_message(year, type, "Analysis", True)

    except :
        display_status_message(year, type, "Analysis", False)

"""
Andrew's Section
WRITING INTO DATABASE FOR PRESENTATION PURPOSES ONLY
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
"""

def chart_data(type, year):
    cluster = MongoClient(
        "mongodb+srv://andrew:1234@cluster0.pgi1d.mongodb.net/CalgaryTraffic?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = cluster["Test"]

    # TRAFFIC MAX
    if type == "Traffic Volume":
        # table_name = f"TrafficVolume{year}"

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
            max = collection.find({}, {'_id': 0, 'volume': 1}).sort('volume', -1).limit(1)
            res = []
            res.append(max[0]['volume'])

    # ACCIDENT MAX
    if type == "Accident":
        res = createGridDict(year, type)[0]["Number of Accidents"]

    return [res]

def map_data(type, year):
    cluster = MongoClient("mongodb+srv://andrew:1234@cluster0.pgi1d.mongodb.net/CalgaryTraffic?ssl=true&ssl_cert_reqs=CERT_NONE")
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
            res[0], res[1] = float(res[1]), float(res[0])

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
            res[0], res[1] = float(res[1]), float(res[0])

        elif year == 2018:
            collection = db.get_collection("TrafficVolume2018")
            max = list(collection.find({}, {'_id': 0,'multilinestring': 1}).sort("volume", -1).limit(1))
            res = []
            tmp = []

            s = max[0]['multilinestring']
            s = s.replace("MULTILINESTRING ((", '')
            tmp = s.split(",")
            s = tmp[0]
            res = s.split()
            res[0], res[1] = float(res[1]), float(res[0])

    # ACCIDENT MAX
    if type == "Accident":
        if year == 2016:
            collection = db.get_collection("Accident2016")
            max = list(collection.find({}, {'_id': 0, 'Longitude' : 1, 'Latitude' : 1}).sort('Latitude', 1))
            res = []
            for i in range(len(max)):
                res.append(tuple([max[i]['Latitude'],max[i]['Longitude']]))

        elif year == 2017:
            collection = db.get_collection("Accident2017")
            max = list(collection.find({}, {'_id': 0, 'Longitude' : 1, 'Latitude' : 1}).sort('Latitude', 1))
            res = []
            for i in range(len(max)):
                res.append(tuple([max[i]['Latitude'],max[i]['Longitude']]))

        elif year == 2018:
            collection = db.get_collection("Accident2018")
            max = list(collection.find({}, {'_id': 0, 'Longitude' : 1, 'Latitude' : 1}).sort('Latitude', 1))
            res = []
            for i in range(len(max)):
                res.append(tuple([max[i]['Latitude'],max[i]['Longitude']]))

    return res

"""
Brandon's Section
"""
class Grid:
    """The Grid class is used for the creation of the map of Calgary for illustrating Accident counts only.
    """
    def __init__(self, minx, maxx, miny, maxy, identifier, name):
        """The first four parameters represent the min and max latitude and longitude in which the grid occupies. 
        count : Stores the number of accidents occuring in the grid
        midX & midY : represents the mid point of the grid to be plotted on the map
        identifier : number identifer of grid
        name : Name of the grid i.e Nosehill, Airport, Downtown
        """
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.count = 0
        self.midX = (minx + maxx) / 2
        self.midY = (miny + maxy) / 2
        self.identifier = identifier
        self.name = name

    def checkPoint(self, points : tuple):
        """checkPoint takes in a list of tuple argument called points and it will pass each x,y coordinate in the list and if the point is located inside the grid specifications, the count increases.
        """
        for x, y in points:
                if (x >= self.minx and x < self.maxx):
                    if(y >= self.miny and y < self.maxy):
                            self.count += 1 

def createGridObjects():
    """createGridObjects divides the City of Calgary into 24 equally sized grid objects, giving them their range, identifier and name. It organizes them into a list consisting the grids.
    return : returns the list of grids.
    """
    startlong = -114.25
    long1 = startlong + 0.09
    long2 = long1 + 0.09
    long3 = long2 + 0.09
    endlong = -113.89

    startlat = 50.85
    lat1 = startlat + 0.06
    lat2 = lat1 + 0.06
    lat3 = lat2 + 0.06
    lat4 = lat3 + 0.06
    lat5 = lat4 + 0.06
    endlat = 51.21

    grid1 = Grid(startlat, lat1, startlong, long1,"1", "Ann & Sandy Conservation")
    grid2 = Grid(startlat, lat1, long1, long2, "2", "Bridlewood SW Calgary")
    grid3 = Grid(startlat, lat1, long2, long3, "3", "Sundance S Calgary")
    grid4 = Grid(startlat, lat1, long3, endlong, "4", "Seton SE Calgary")

    grid5 = Grid(lat1, lat2, startlong, long1,"5", "Fish Creek River")
    grid6 = Grid(lat1, lat2, long1, long2,"6", "Fish Creek Pronvince Park")
    grid7 = Grid(lat1, lat2, long2, endlong,"7", "Lake Bonavista & Shepard Industrial")
    grid8 = Grid(lat1, lat2, long3, endlong,"8", "McKenzie Towne & New Brighton")

    grid9 = Grid(lat2, lat3, startlong, long1,"9", "Discovery Ridge")
    grid10 = Grid(lat2, lat3, long1, long2,"10", "Mount Royal Univeristy & West Glenmore Trail")
    grid11 = Grid(lat2, lat3, long2, endlong,"11", "Deerfoot & East Glenmore Trail")
    grid12 = Grid(lat2, lat3, long3, endlong,"12", "East Calgary Landfill Area")

    grid13 = Grid(lat3, lat4, startlong, long1,"13", "Sarcee Trail & Coach Hill")
    grid14 = Grid(lat3, lat4, long1, long2,"14", "West Downtown Area & Crowchild Trail")
    grid15 = Grid(lat3, lat4, long2, long3,"15", "East Downtown Area & Memorial Drive & Deerfoot Trail")
    grid16 = Grid(lat3, lat4, long3, endlong,"16", "16th Avenue East and Stoney Trail")

    grid17 = Grid(lat4, lat5, startlong, long1,"17", "Crowchild Trail & Stoney Trail NW Calgary")
    grid18 = Grid(lat4, lat5, long1, long2,"18", "Nose Hill")
    grid19 = Grid(lat4, lat5, long2, long3,"19", "Deerfoot & Airport Area")
    grid20 = Grid(lat4, lat5, long3, endlong,"20", "McKnight Boulevard & Stoney Trail NE Calgary")

    grid21 = Grid(lat5, endlat, startlong, long1,"21", "SpyHill & Stoney Trail")
    grid22 = Grid(lat5, endlat, long1, long2,"22", "Evanston & Stoney Trail")
    grid23 = Grid(lat5, endlat, long2, long3,"23", "Deerfoot Trail & Stoney Trail North Calgary")
    grid24 = Grid(lat5, endlat, long3, endlong,"24", "Skyview Area & Stoney Trail")  

    grids = [grid1, grid2, grid3, grid4, grid5, grid6, grid7, grid8, grid9, grid10, grid11, grid12, grid13, grid14, grid15, grid16, grid17, grid18, grid19, grid20, grid21, grid22, grid23, grid24]
    return grids

def getGridCount(grid):
    return grid.count   

def get_geojson_grid(upper_right, lower_left, n, m):
    """Returns a grid of geojson rectangles, and computes the exposure in each section of the grid based on the vessel data.
    Parameters
    ----------
    upper_right: array_like
        The upper right hand corner of "grid of grids" (the default is the upper right hand [lat, lon] of the USA).
    lower_left: array_like
        The lower left hand corner of "grid of grids"  (the default is the lower left hand [lat, lon] of the USA).
    n: integer
        The number of rows/columns in the (n,n) grid.
    list
        List of "geojson style" dictionary objects   
    """
    all_boxes = []

    lat_steps = np.linspace(lower_left[0], upper_right[0], n+1)
    lon_steps = np.linspace(lower_left[1], upper_right[1], m+1)

    lat_stride = lat_steps[1] - lat_steps[0]
    lon_stride = lon_steps[1] - lon_steps[0]

    for lat in lat_steps[:-1]:
        for lon in lon_steps[:-1]:
            # Define dimensions of box in grid
            upper_left = [lon, lat + lat_stride]
            upper_right = [lon + lon_stride, lat + lat_stride]
            lower_right = [lon + lon_stride, lat]
            lower_left = [lon, lat]

            # Define json coordinates for polygon
            coordinates = [
                upper_left,
                upper_right,
                lower_right,
                lower_left,
                upper_left
            ]

            geo_json = {"type": "FeatureCollection",
                        "properties":{
                            "lower_left": lower_left,
                            "upper_right": upper_right
                        },
                        "features":[]}

            grid_feature = {
                "type":"Feature",
                "geometry":{
                    "type":"Polygon",
                    "coordinates": [coordinates],
                }
            }

            geo_json["features"].append(grid_feature)
            all_boxes.append(geo_json)

    return all_boxes

def createMapVolume(x,y): #
    """createMapVolume is called when the user wants to create a map of the city with the highest volume location marked. A x and y coordinate is accepted for arguments and a marker is added onto the map, and then the map is saved into the current working directory.
    """
    m = folium.Map(
        location=[51.0447, -114.0719], #Coordinates of Calgary
        zoom_start=12   
    )
    tooltip = 'Click me!'
    folium.Marker([x, y], popup='<i>his area has the highest volume of traffic!</i>', tooltip=tooltip).add_to(m)
    m.save('map.html')

def createMarkerAccident(grid : Grid, m :map):
    """Creates a pin on the map with the coordinates cooresponding to the midpoint of the grid with the highest accident count. A grid object and a map object are passed as arguments for this function.
    """
    tooltip = 'Click me!'
    folium.Marker([grid.midX, grid.midY], popup=grid.name, tooltip=tooltip).add_to(m)

def createGridDict(year, type):
    """ createGridDict function is used when the user is sorting the Accident information from the tables. We sort the grids after running the grid object's checkPoint function and then we create and return a dictionary of the grids.
    """
    grids = createGridObjects()
    dataList = map_data(type, year)
    for grid in grids: 
        grid.checkPoint(dataList) #Passing the list of coordinates for each grid section

    sortedGrids = sorted(grids, key = getGridCount, reverse= True)
    gridDict = [{'Grid Identifier': grid.identifier, 'Area': grid.name, 'Number of Accidents':grid.count} for grid in sortedGrids]
    return gridDict

def createMapAccident(dataList):
    """createMapAccident will accepts a dataList of coorindates of all the accidents for that year and then create a marker on the grid with the highest accident count. Then call the get_geojson_grid function to create a 4x6 grid on the map. Lastly we create and save the map.html file on the working directory.
    """
    #Creates map of Calgary
    m = folium.Map(
        location=[51.0447, -114.0719], #Coordinates of Calgary
        zoom_start=12   
    )

    #Generate GeoJson Grid
    startlong = -114.25
    endlong = -113.89
    startlat = 50.85
    endlat = 51.21

    grids = createGridObjects()

    for grid in grids: 
        grid.checkPoint(dataList) #Passing the list of coordinates for each grid section

    sortedGrids = sorted(grids, key = getGridCount, reverse= True)
    createMarkerAccident(sortedGrids[0],m)
    lowerLeft = [startlat, startlong]
    upperRight = [endlat, endlong]
    gridLines = get_geojson_grid(upperRight, lowerLeft,6,4)

    for i, geo_json in enumerate(gridLines):

        gj = folium.GeoJson(geo_json,
                            style_function=lambda feature: {
                                                                            'color':"black",
                                                                            'weight': 2,
                                                                            'dashArray': '5, 5',
                                                                            'fillOpacity': 0.01,
                                                                        })
        m.add_child(gj)

    m.save('map.html') #Creates a html file in my User Directory

def mapButton():
    """When the user clicks the Map button the GUI, mapButton function is called. Here the function will obtain the type of data and year selected and call the associated functions createMapAccident or createMapVolume.
    """
    try:
        type = get_year_and_type()[0]
        year = int(get_year_and_type()[1])

        if type == "Accident":
            createMapAccident((map_data(type,year)))
    
        if type == "Traffic Volume":
            res = map_data(type,year)
            x = res[0]
            y = res[1]
            createMapVolume(x,y)

        display_status_message(year, type, button= "Map", is_success = True)
        
    except:
        display_status_message(year, type, button= "Map", is_success = False)

#GUI Interface Code Block
window = tk.Tk()
window.title("Calgary Traffic Analysis")
window.geometry('800x500')

window.rowconfigure(0, minsize = 50, weight = 1)
window.columnconfigure(1, minsize = 50, weight =1)

frm_buttons = tk.Frame(window)
frm_display = tk.Frame(window)
frm_display.rowconfigure(0, minsize = 100, weight =1)
frm_display.columnconfigure(0, minsize = 100, weight = 1)

# left frame
#combo box for type
com_box_type = ttk.Combobox(frm_buttons, values = ["Accident", "Traffic Volume"] )
com_box_type.current(0)
com_box_type.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "ew")

#combo box for year
com_box_year = ttk.Combobox(frm_buttons, values = ["2016", "2017", "2018"] )
com_box_year.current(0)
com_box_year.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "ew")

# button for Read
btn_read = tk.Button(frm_buttons, text = "Read", command = display_table)
btn_read.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "ew")

# button for Sort
btn_sort = tk.Button(frm_buttons, text = "Sort", command = display_sorted_table)
btn_sort.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "ew")

# button for Analysis
btn_analysis = tk.Button(frm_buttons, text = "Analysis", command = display_chart)
btn_analysis.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "ew")

# button for Map
btn_map = tk.Button(frm_buttons, text = "Map", command = mapButton)
btn_map.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = "ew")

# label for Status
lbl_status = tk.Label(frm_buttons, text = "Status:")
lbl_status.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "ew")

# label for Status display
lbl_status_display = tk.Label(frm_buttons, text = "---", bg = "green",  wraplength = 150)
lbl_status_display.grid(row = 7, column = 0, padx = 5, pady = 5, sticky = "ew")

#right frame
txt_display = tk.Text(frm_display)
txt_display.grid(sticky = "nsew")

# position left and right frame 
frm_buttons.grid(row =0, column = 0, sticky = "ns")
frm_display.grid(row =0, column = 1, sticky = "nsew" )

window.mainloop()

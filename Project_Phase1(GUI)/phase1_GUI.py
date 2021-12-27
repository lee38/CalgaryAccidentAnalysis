import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# data for all incidents
df_incidents = pd.read_csv("Traffic_Incidents.csv")
df_incidents['START_DT'] = pd.to_datetime(df_incidents['START_DT'])

# data for traffic volumes
# 2016
df_2016_volume = pd.read_csv("TrafficFlow2016_OpenData.csv")

#2017
df_2017_volume = pd.read_csv("2017_Traffic_Volume_Flow.csv")

#2018
df_2018_volume = pd.read_csv("Traffic_Volumes_for_2018.csv")


def get_year_and_type():
    '''gets the year and type selection from the combo boxes
    '''
    year = com_box_year.get()
    type = com_box_type.get()
    print(type, year)
    return type, year

def display_chart():
    '''reads combo box selection and displays chart
    '''
    # get type and year from combo box 
    type = get_year_and_type()[0]
    year = get_year_and_type()[1]

    # create figure
    figure1 = plt.Figure(figsize=(5,5), dpi=70)
    ax = figure1.add_subplot(111)

    # add figure to frame
    canvas = FigureCanvasTkAgg(figure1, frm_display)
    canvas.get_tk_widget().grid(row =0, column = 0, sticky = "nsew")

    
    df_count = df_incidents[["START_DT", "Count"]].groupby(df_incidents["START_DT"].dt.year).sum().reset_index()

    x = df_count["START_DT"]
    y = df_count["Count"]
    label = "number of accidents"
    ax.plot(x, y, marker ='*', label = label)
    ax.legend()
    ax.set_title('number of accidents vs Year')
    ax.set_xlabel('Year')
    ax.set_ylabel('incidents')

    

    
    

def display_table():
    '''reads combo box selection and displays table
    '''
    type = get_year_and_type()[0]
    year = int(get_year_and_type()[1])

    # select data to display in table 
    if type == "Accident":
        data = df_incidents.loc[df_incidents["START_DT"].dt.year == year,:]

    if type == "Traffic Volume":
        if year == 2016:
            data = df_2016_volume
        elif year == 2017:
            data = df_2017_volume
        elif year == 2018:
            data = df_2018_volume

    # create and add tree (table) to frame
    tree = ttk.Treeview(frm_display, columns = data.columns, height = 20, show = "headings")
    tree.grid(row = 0, column = 0, sticky = "nsew")

    # configure tree (table) heading and column display
    for i in range(data.shape[1]):
        tree.heading(i, text = data.columns[i])
        tree.column(i, anchor = "center", width = 150)

    # add data rows to table  
    for _, row in data.iterrows():
        tree.insert('', 'end', values = [column_data for column_data in row])

    # scroll bars
    scroll_y = ttk.Scrollbar(frm_display, orient="vertical", command=tree.yview)
    scroll_y.grid(row =0, column =1, sticky = "ns")

    scroll_x = ttk.Scrollbar(frm_display, orient="horizontal", command= tree.xview)
    scroll_x.grid(row =1, column =0, sticky = "ew")

    tree.configure(yscroll = scroll_y.set, xscroll = scroll_x.set)

    



window = tk.Tk()
window.title("Calgary Traffic Analysis")
# window.geometry('350x250')

window.rowconfigure(0, minsize = 50, weight = 1)
window.columnconfigure(1, minsize = 50, weight =1)

frm_buttons = tk.Frame(window)
frm_display = tk.Frame(window)

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
btn_sort = tk.Button(frm_buttons, text = "Sort")
btn_sort.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = "ew")

# button for Analysis
btn_analysis = tk.Button(frm_buttons, text = "Analysis", command = display_chart)
btn_analysis.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "ew")

# button for Map
btn_map = tk.Button(frm_buttons, text = "Map")
btn_map.grid(row = 5, column = 0, padx = 5, pady = 5, sticky = "ew")

# label for Status
lbl_status = tk.Label(frm_buttons, text = "Status:")
lbl_status.grid(row = 6, column = 0, padx = 5, pady = 5, sticky = "ew")

# label for Status display
lbl_status_display = tk.Label(frm_buttons, text = "---", bg = "green")
lbl_status_display.grid(row = 7, column = 0, padx = 5, pady = 5, sticky = "ew")

#right frame
txt_display = tk.Text(frm_display)
txt_display.grid(sticky = "nsew")

# position left and right frame 
frm_buttons.grid(row =0, column = 0, sticky = "ns")
frm_display.grid(row =0, column = 1, sticky = "nsew" )


window.mainloop()
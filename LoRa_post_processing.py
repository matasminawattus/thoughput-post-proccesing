# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 20:03:26 2021

@author: matas.kirstukas

Wireless Data Throughput Test Post Processing
"""

import serial
import time
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pickle

title = 'Max_Speed_Test_1_05_05'
df = pd.read_excel(title+'.xlsx')

SPI = df['SPI']
LORA = df['Lora']
BLORA = df['Boat Lora']
RSSI = df['RSSI']
LAT = df['Latitude']
LON = df['Longitude']
# SPEED = df['Speed']

# setting = df.iloc[0]['setting']

#%%
import gmplot

def build_color(r, g, b):
    color = "#"
    for num in [r, g, b]:    
        color += (hex(num)[2:] if len(hex(num)[2:]) > 1 else "0" + hex(num)[2:])
    return color

import matplotlib
#%%
cmap = matplotlib.cm.get_cmap('viridis')
norm = matplotlib.colors.Normalize(vmin=0.0, vmax=160.0)


# Create the map plotter:
apikey = 'AIzaSyClb0TMlQJyl2XAJ0c3JvI2t7e9417vo2o' # (your API key here)
gmap = gmplot.GoogleMapPlotter(54.697698, 25.309917, 18, apikey=apikey)


fromto = [0, -1]
COLOR = []
    
bounds = {'north': np.max(LAT), 
          'south': np.min(LAT), 
          'east':  np.max(LON), 
          'west':  np.min(LON)}

gmap = gmplot.GoogleMapPlotter(np.mean(LAT), np.mean(LON), 18, apikey=apikey, fit_bounds=bounds)
# gmap.heatmap(latitude, longitude)

for r in SPI:
    color = cmap(norm(r))
    c = build_color(int(color[0]*255),
                    int(color[1]*255),
                    int(color[2]*255))
    COLOR.append(c)

gmap.scatter(LAT[fromto[0]:fromto[1]], LON[fromto[0]:fromto[1]], color=COLOR[fromto[0]:fromto[1]], s=2, marker=False)

# Draw the map:
gmap.draw(title+'.html')

#%%
df = df[0:]
import geopy.distance
import chart_studio.plotly as py
import chart_studio
chart_studio.tools.set_credentials_file(username='matas.kirstukas', api_key='0uFDaHfiO3RsNctInSSj')

df['Speed'] = df['SPI']*250*8
# df['bitrate'] = df['received']
df['distance'] = [geopy.distance.geodesic((df['Latitude'].iloc[0],df['Longitude'].iloc[0]),(x, y)).m for x, y in zip(df['Latitude'], df['Longitude'])]
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
px.set_mapbox_access_token("pk.eyJ1Ijoic3RydXRpcyIsImEiOiJja3Z1cHRudWM1OHF3MndxNWdsNTBlM2NqIn0.qM_heUcaeVPR8pQ8kYtcQA")
#df = px.data.carshare()
fig = px.scatter_mapbox(df, 
                        lat="Latitude", 
                        lon="Longitude",  
                        color="Speed", 
                        hover_data = ['distance',],
                        size_max=15, 
                        zoom=18)

fig.write_html(title+'.html',include_plotlyjs="cdn")

df.to_excel(title+'_processed.xlsx')

fig.show()
#py.plot(fig, filename = 'zalieji 05-10', auto_open=True)
url=py.plot(fig, filename = title, auto_open=True)

#%%
plt.figure()
plt.scatter(LON,LAT,c=COLOR)

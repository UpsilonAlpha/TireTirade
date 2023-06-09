import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pyproj
import json
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely import wkt
import scipy.signal as sig
from scipy.fftpack import fft
from scipy.io import wavfile

MAPBOX_ACESSTOKEN = "pk.eyJ1IjoiZm9yc3dvcm4iLCJhIjoiY2xnd2NpemVpMmt2bzNsbGg5ZHdtcDdqbCJ9.71Qy9AEmPQd48pDPbJ4quw"

df = pd.read_csv("TireRecycling.csv")
df = df[["Year", "Jurisdiction", "Type", "Stream", "Management", "Tonnes"]]
df = df[df["Type"] == "Tyres (T140)"]
df = df[df["Stream"]=="Total"]
df = df.replace(',','', regex=True)
df['Tonnes'] = df['Tonnes'].apply(pd.to_numeric)
df = df[df['Tonnes'] > 0]
df = df[df['Management'] != "Other disposal"]
df = df[::-1]

for i in range(len(df["Year"])):
    year = df.iloc[i,0]
    df.iloc[i,0] = year[5:9]
print(df['Year'])
df['Year'] = df['Year'].apply(pd.to_numeric)

df = df[df["Year"]>2011]
df = df[["Year", "Jurisdiction", "Management", "Tonnes"]]

recycled = df[df["Management"] == "Recycling"]
burned = df[df["Management"] == "Energy from waste facility"]
landfill = df[df["Management"] == "Landfill"]

percent_recycled = ((recycled["Tonnes"].values)/(recycled["Tonnes"].values + burned["Tonnes"].values+landfill["Tonnes"].values))*100
percent_burned = ((burned["Tonnes"].values)/(recycled["Tonnes"].values + burned["Tonnes"].values+landfill["Tonnes"].values))*100
percent_landfill = ((landfill["Tonnes"].values)/(recycled["Tonnes"].values + burned["Tonnes"].values+landfill["Tonnes"].values))*100

recycled["Tonnes"] = percent_recycled
burned["Tonnes"] = percent_burned
landfill["Tonnes"] = percent_landfill

df[df["Management"] == "Recycling"] = recycled
df[df["Management"] == "Energy from waste facility"] = burned
df[df["Management"] == "Landfill"] = landfill

print(df)
df.to_csv("CleanRecycling.csv")


df = pd.read_csv("PercentRecycling.csv")
line = px.line(df[df["Management"]=="Landfill"], y="Tonnes", x="Year", color="Jurisdiction" )
line.show()
df["geometry"] = gpd.GeoSeries()
df = df[["geometry", "Year", "Jurisdiction", "Management", "Tonnes"]]
states = gpd.read_file("STE_2021_AUST_GDA2020.shp")

for i in range(len(df["Jurisdiction"])):
    
    match df.iloc[i,2]:
        case "NSW":
            df.iloc[i, 0] = states.iloc[0, 8]
        case "Vic":
            df.iloc[i, 0] = states.iloc[1, 8]
        case "Qld":
            df.iloc[i, 0] = states.iloc[2, 8]
        case "SA":
            df.iloc[i, 0] = states.iloc[3, 8]
        case "WA":
            df.iloc[i, 0] = states.iloc[4, 8]
        case "Tas":
            df.iloc[i, 0] = states.iloc[5, 8]
        case "NT":
            df.iloc[i, 0] = states.iloc[6, 8]
        case "ACT":
            df.iloc[i, 0] = states.iloc[7, 8]




gdf = gpd.GeoDataFrame(df)
gpd.GeoDataFrame.set_geometry(gdf, gdf["geometry"])
gdf.crs = "EPSG:7844"

gdf.to_crs(epsg=4326)
gjson = gdf.__geo_interface__

print(gdf)

with open('PercentStates.geojson', 'w') as fp:
    json.dump(gjson, fp)


df = pd.read_csv("CleanRecycling.csv")
print(df)

with open ("States.geojson",'r') as infile:
    gjson = json.load(infile)

recycling = df[df["Management"]=="Recycling"]
burned = df[df["Management"]=="Energy from waste facility"]
landfill = df[df["Management"]=="Landfill"]
print(df)
chloropleth = px.choropleth(recycling, geojson=gjson, locations=recycling.index, color="Tonnes", animation_frame="Year", center=dict(lat=-26.5 , lon=135.5),color_continuous_midpoint=25000)
chloropleth.update_geos(fitbounds="locations")
area = px.area(recycling, y="Tonnes", x="Year", color="Jurisdiction")

chloropleth.update_layout(
    updatemenus=[
        dict(
            type = "buttons",
            direction = "left",
            active= -1,
            buttons=list([
                dict(
                    args=[{"visible": [True,False]}, {"type":"choropleth"}],
                    label="Choropleth",
                    method="update"
                ),
                dict(
                    args=[{"visible": [False,True]}, {"type":"area"}],
                    label="Area",
                    method="update"
                )
            ]),
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.11,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)


chloropleth.show()
area.show()





fs, new = wavfile.read("RoadNoise.wav")
fs, old = wavfile.read("RoadNoise.wav")
a = wav.T[0]

b = fft(a) # calculate fourier transform (complex numbers list)
c = int(len(b)/4)  # you only need half of the fft list (real signal symmetry)

k = np.arange(c-1)
T = len(wav)/fs
frqLabel = k/T

y = sig.savgol_filter(b, 100, 3)
fig = px.line(y=abs(y[:(c-1)]), x=frqLabel, log_x=True)
fig.update_layout(xaxis_range=[1,4])
fig.show()


b = np.array_split(a, 10)

i=0
for frame in b:
    frame = fft(frame)
    frame = np.array_split(frame,2)
    b[i] = np.abs(frame[0])
    i +=1

#c = pd.DataFrame(b)
c = pd.DataFrame(range(0,10))
c.insert(1, "frame", range(0,10), True)
c.insert(2,"data", b, True)

print(c)

c=int(len(b[9]/2))
d=[]
for i in range(0,9):
    d.append(fft(b[i]))
    d[i] = np.abs(d[i][:(c-1)])

e=pd.DataFrame(range(0,9))
e.insert(1, "frame", range(0,9), True)
e.insert(2, "data", d, True)


c=pd.DataFrame(range(0,142830))

freqs = []
e = []
frames = []
for i in range(1,10):
    for num in range(0,15870):
        freqs.append(num)
        frames.append(f"Frame{i}")
    d = fft(b[i])
    d2 = np.abs(d[:int(len(d)/2)-1])
    #d3 = sig.savgol_filter(d2, 5, 3)
    for x in np.abs(d2[:int(len(d2/2)-1)]):
        e.append(x/20000000)
    

c.insert(0, "Frequencies", freqs)
c.insert(1, "Frames", frames)
c.insert(2, "Values", e)
c.to_csv("RoadNoise.csv")

fig = px.line(c,x ="Frequencies", y="Values",animation_frame="Frames", log_x=True)
fig.update_layout(xaxis_title="Frequency (Hz)", yaxis_title="Relative Amplitude",yaxis_range=[0,1])
fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 666
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 666
#fig = go.Figure(go.Scatter(y=c.iloc[:,1]), log_x=True)
fig.show()




fs1, old = wavfile.read("RoadNoise.wav")
fs2, new = wavfile.read("OldNoise.wav")

a1 = old.T[0]
a2 = new.T[0]


b1 = fft(a1) 
b2 = fft(a2) 

b1 = b1[0:293342]


freqs = []
e = []
frames = []


d1 = np.abs(b1[:int(len(b1)/2)-1])
d2 = np.abs(b2[:int(len(b2)/2)-1])
d1 = sig.savgol_filter(d1, 100, 3)
d2 = sig.savgol_filter(d2, 100, 3)
for x in np.abs(d1[:int(len(d1/2)-1)]):
    e.append(x/25000000)
    frames.append("1920s Tires")
for x in np.abs(d2[:int(len(d2/2)-1)]):
    e.append(x/25000000)
    frames.append("Modern Tires")
for num in range(1,146670):
    freqs.append(num)
for num in range(1,146670):
    freqs.append(num)

c=pd.DataFrame(range(0,293338))
c.insert(0, "Frequencies", freqs)
c.insert(1, "Type", frames)
c.insert(2, "Values", e)

c.to_csv("OldNoise.csv")
print(c)
'''
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyodide.http import open_url
from pyodide.ffi import create_proxy
from js import Plotly, JSON, document
import urllib, json

url1 = ("https://raw.githubusercontent.com/UpsilonAlpha/TireTirade/main/TireData.csv")
tire_data = pd.read_csv(open_url(url1))

url2 = ("https://raw.githubusercontent.com/UpsilonAlpha/TireTirade/main/OldNoise.csv")
road_noise = pd.read_csv(open_url(url2))

#url3 = ("https://raw.githubusercontent.com/UpsilonAlpha/TireTirade/main/PercentRecycling.csv")
#df = pd.read_csv(open_url(url3))

url4 = ("https://raw.githubusercontent.com/UpsilonAlpha/TireTirade/main/CleanRecycling.csv")
df = pd.read_csv(open_url(url4))
recycling = df[df["Management"]=="Recycling"]
landfill = df[df["Management"]=="Landfill"]

url5 = ("https://raw.githubusercontent.com/UpsilonAlpha/TireTirade/main/States.geojson")
gjson = json.loads(open_url(url5).getvalue())

template = "plotly"

def show_output(*args, **kwargs):
    output = getElementById("output_div")
    output.innerHTML = "You Clicked Me!"
    template = "plotly_dark"

'''
def lights():
    template = "plotly_dark"
    bar.update_layout(template=template)
    pie.update_layout(template=template)
    sankey.update_layout(template=template)
    Plotly.react('bar', JSON.parse(bar.to_json()))
    Plotly.react('pie', JSON.parse(pie.to_json()))
    Plotly.react('sankey', JSON.parse(sankey.to_json()))


function_proxy = create_proxy(lights)
document.getElementById("button").addEventListener("click", function_proxy)
#<button type="button" id="button">Change theme</button>
'''

#Where do degraded tires go?
bar = go.Figure([go.Bar(x=tire_data["System"], y=tire_data["Tonnes"], error_y=dict(type='percent', value=10, visible=True))])
bar.update_layout(title_x=0.5,title="Where do tire microplastics enter the environment?", xaxis_title="Pathway", yaxis_title="Tonnes")
Plotly.react('bar', JSON.parse(bar.to_json()))

#What is the average car tyre made of?
pie = px.sunburst(tire_data, width=700, height=700,values="Kilograms", names="Materials",parents="Parent",template=template, branchvalues="remainder", title="What are tires made of?")
pie.update_layout(title_x=0.5)
Plotly.react('pie', JSON.parse(pie.to_json()))


#How much energy is wasted by friction?
sankey = go.Figure(go.Sankey(
    arrangement="snap",
    node={"label":['Transmission','Wheels','Transmission loss','Rolling resistance', 'Air resistance', 'Braking'], 
                                "x":[0,0.1,0.1,0.2,0.2,0.2],
                                "y":[0, 0, -0.1,0,0,0],},
                                link={"source":[0,0,1,1,1],
                                "target":[1,2,3,4,5],
                                "value":[0.21, 0.02,0.073, 0.112,0.025]}, hoverinfo='skip'))
sankey.update_layout(title_text="How is energy lost from the transmisson of a car?", title_x=0.5, template=template)

Plotly.react('sankey', JSON.parse(sankey.to_json()))

'''
fourier = px.line(road_noise, x ="Frequencies", y="Values",animation_frame="Frames", log_x=True)
fourier.update_layout(xaxis_title="Frequency (Hz)", yaxis_title="Relative Amplitude",yaxis_range=[0,1])
fourier.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 666
fourier.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 666
'''
fourier = px.line(road_noise,x="Frequencies", y="Values",animation_frame="Type", log_x=True)
fourier.update_layout(xaxis_title="Frequency (Hz)", yaxis_title="Relative Amplitude",yaxis_range=[0,1], title_x=0.5, template=template, title_text="What does the noise profile of cars with different tires look like?")
Plotly.react('fourier', JSON.parse(fourier.to_json()))




chloropleth = px.choropleth(recycling, geojson=gjson, locations=recycling.index, color="Tonnes", animation_frame="Year", center=dict(lat=-26.5 , lon=135.5),color_continuous_midpoint=25000)
chloropleth.update_geos(fitbounds="locations")

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
chloropleth.update_layout(title_x=0.5,title="How many tonnes of tire waste are recycled in each state?")

Plotly.react('chloropleth', JSON.parse(chloropleth.to_json()))

area = px.area(landfill, y="Tonnes", x="Year", color="Jurisdiction")
area.update_layout(title_x=0.5,title="How many tonnes of tire waste goes into landfill from each state?")
Plotly.react('area', JSON.parse(area.to_json()))

scatter = px.scatter(tire_data, x="FSI", y="Emissions", size=tire_data["Capacity"].apply(pd.to_numeric), size_max=60, color="Method")
scatter.update_layout(title_x=0.5,title="A comparison of FSI, Emissions and Corridor Capacity", xaxis_title="Fatalities and Serious Injuires per Year", yaxis_title="CO2 Emissions (g/km)")
Plotly.react('scatter', JSON.parse(scatter.to_json()))
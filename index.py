import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyodide.http import open_url
from pyodide.ffi import create_proxy
from js import Plotly, JSON, document

url1 = ("https://raw.githubusercontent.com/UpsilonAlpha/TireTirade/main/TireData.csv")
tire_data = pd.read_csv(open_url(url1))

url2 = ("https://raw.githubusercontent.com/UpsilonAlpha/TireTirade/main/RoadNoise.csv")
road_noise = pd.read_csv(open_url(url2))

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
bar = px.bar(tire_data, x="System", y="Tonnes", template=template,title="Where do tire microplastics enter the environment?")
bar.update_layout(title_x=0.5)
Plotly.react('bar', JSON.parse(bar.to_json()))

#What is the average car tyre made of?
pie = px.sunburst(tire_data, width=700, height=700,values="Kilograms", names="Materials",parents="Parent",template=template, branchvalues="remainder", title="What are tires made of?")
pie.update_layout(title_x=0.5)
Plotly.react('pie', JSON.parse(pie.to_json()))


#How much energy is wasted by friction?
sankey = go.Figure(go.Sankey(
    arrangement="snap",
    node={"label":['Transmission','Wheels','Transmission loss','Rolling resistance', 'Air resistance', 'Braking'], 
                                "x":[0,0.1,0,0.2,0.2,0.2],
                                "y":[0, 0, -0.1,0,0,0]},
                                link={"source":[0,0,1,1,1],
                                "target":[1,2,3,4,5],
                                "value":[0.21, 0.02,0.073, 0.112,0.025]}))
sankey.update_layout(title_text="How is energy lost from the transmisson of a car?", title_x=0.5, template=template)

Plotly.react('sankey', JSON.parse(sankey.to_json()))


fourier = px.line(road_noise, x ="Frequencies", y="Values",animation_frame="Frames", log_x=True)
fourier.update_layout(xaxis_title="Frequency (Hz)", yaxis_title="Relative Amplitude",yaxis_range=[0,1])
fourier.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 666
fourier.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 666
fourier.update_layout(title_text="What does the noise profile of a car look like?", title_x=0.5, template=template, xaxis_title="Frequency (Hz)", yaxis_title="Amplitude (dB)")
Plotly.react('fourier', JSON.parse(fourier.to_json()))


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyodide.http import open_url
from pyodide.ffi import create_proxy
from js import Plotly, JSON, document

url = ("https://raw.githubusercontent.com/UpsilonAlpha/TireTirade/main/TireData.csv")
tire_data = pd.read_csv(open_url(url))

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
pie = px.sunburst(tire_data, values="Kilograms", names="Materials",parents="Parent",template=template, branchvalues="remainder", title="What are tires made of?")
pie.update_layout(title_x=0.5)
Plotly.react('pie', JSON.parse(pie.to_json()))


#How much energy is wasted by friction?
sankey = go.Figure(go.Sankey(
    arrangement="snap",
    node={"label":['Transmission','Wheels','Transmission loss','Rolling resistance', 'Air resistance', 'Braking'], 
                                "x":[0,0.1,0,0.2,0.2,0.2],
                                "y":[0, 0, 0.1,0,0,0]},
                                link={"source":[0,0,1,1,1],
                                "target":[1,2,3,4,5],
                                "value":[0.21, 0.02,0.073, 0.112,0.025]}))
sankey.update_layout(title_text="How is energy lost from the transmisson of a car?", title_x=0.5, template=template)

Plotly.react('sankey', JSON.parse(sankey.to_json()))


'''
fs, wav = wavfile.read(open_url(url))
a = wav.T[0]
b = np.array_split(a, 10)
c=pd.DataFrame(range(0,15871))
for i in range(1,10):
    d = fft(b[i])
    c.insert(i,f"data{i}",np.abs(d[:int(len(d)/2)-1]))

fourier = px.line(c, y=(c.iloc[:,1]/100000), log_x=True)
fourier.update_layout(title_text="What does the noise profile of a car look like?", title_x=0.5, template=template, xaxis_title="Frequency (Hz)", yaxis_title="Amplitude (dB)")
Plotly.react('fourier', JSON.parse(fourier.to_json()))
'''
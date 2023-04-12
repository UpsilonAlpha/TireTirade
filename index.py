import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyodide.http import open_url
from js import Plotly, JSON

url = ("https://raw.githubusercontent.com/UpsilonAlpha/Library/master/University/COSC3000/DataVis/TireData.csv?token=GHSAT0AAAAAAB67B64KNWX5AZISIDL4NWFQZBDTNRA")
#tire_data = pd.read_csv(open_url(url))
'''


#Where do degraded tires go?
fig = px.bar(tire_data, x="System", y="Tonnes")
Plotly.react('bar', JSON.parse(fig.to_json()))

#What is the average car tyre made of?
fig = px.pie(tire_data, values="Kilograms", names="Materials", hole=0.5)
Plotly.react('pie', JSON.parse(fig.to_json()))
'''
#How much energy is wasted by friction?
fig = go.Figure(go.Sankey(node={"label":['Transmission','Wheels','Transmission loss','Rolling resistance', 'Air resistance', 'Braking'], "x":[0,0.2,0.2,0.3,0.3,0.3], "y":[0, 0, 0.7,0.5,0.3,0.1]}, link={"source":[1,1,1,2,2,2], "target":[2,3,3,4,5,6], "value":[0.23, 0.21, 0.02,0.073, 0.112,0.025]}))
fig.show()
#plotly.react('sankey', JSON.parse(fig.to_json()))

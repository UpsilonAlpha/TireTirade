import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
from scipy.fftpack import fft
from scipy.io import wavfile

fs, wav = wavfile.read("RoadNoise.wav")
a = wav.T[0]
'''
b = fft(a) # calculate fourier transform (complex numbers list)
c = int(len(b)/4)  # you only need half of the fft list (real signal symmetry)

k = np.arange(c-1)
T = len(wav)/fs
frqLabel = k/T

y = sig.savgol_filter(b, 100, 3)
fig = px.line(y=abs(y[:(c-1)]), x=frqLabel, log_x=True)
fig.update_layout(xaxis_range=[1,4])
fig.show()
'''

b = np.array_split(a, 10)
'''
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

'''
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

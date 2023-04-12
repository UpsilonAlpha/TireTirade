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
c=pd.DataFrame(range(0,15871))
for i in range(1,10):
    d = fft(b[i])
    c.insert(i,f"data{i}",np.abs(d[:int(len(d)/2)-1]))

#fig = px.scatter(c, y=c.columns, animation_frame=0, log_x=True, )
fig = go.Figure(go.Scatter(y=c.iloc[:,1]))
fig.show()
fig.update(y=c.iloc[:,2])
fig.show()
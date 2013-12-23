# -*- coding: utf-8 -*-
import pyaudio
import wave

from scipy import arange
from numpy import pi
from pylab import cos
from matplotlib import pyplot

freq = 500.0
sam_rate=6000.0
N     = 6000
T     = arange(0.0,float(N),1.0)
xArray = cos(2.0*pi*freq*T/sam_rate) * 256
xArray.astype(int)

#chunk = 1024

#wf = wave.open(r"c:\WINDOWS\Media\ding.wav", 'rb')

p = pyaudio.PyAudio()
fig1 = pyplot.figure()

# open stream
#channel = wf.getnchannels()
channel = 1
#rates = wf.getframerate()
rates = int(sam_rate)
#format1 = p.get_format_from_width(wf.getsampwidth())
format1 = 8 #this means 16bit int?

stream = p.open(format = format1,
                channels=channel,
                rate=rates,
                output = True)

# write stream to play
phase = pi/2
counter = 200
xArray = cos(2.0*pi*freq*T/sam_rate + phase) * 2048
data = xArray.astype(int)
while True:
    #data = wf.readframes(chunk)
    stream.write(data)
    xArray = cos(2.0*pi*freq*T/sam_rate + phase) * 1000
    data = xArray.astype(int)
    counter = counter - 1
    if counter == 0: break
    #pyplot.plot(data)
    #pyplot.show()


stream.close()
p.terminate()

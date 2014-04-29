# -*- coding: utf-8 -*-
import pyaudio
import wave
import time
from struct import *

from scipy import arange
from numpy import pi
from pylab import cos,sin
from matplotlib import pyplot

freq = 100
sam_rate=44100
N     = 44100
T     = range(0,sam_rate/freq,1)
Amp   = 32000
Sample_Len = 5

p = pyaudio.PyAudio()
fig1 = pyplot.figure()

channel = 1
rates = int(sam_rate)
format1 = pyaudio.paInt16

phase = pi/2
phase = 0
counter = 2
xArray = ""
datalst = []

for j in range(Sample_Len):
    for i in T:
        tempf=sin(2.0*pi*float(freq)*float(i)/float(sam_rate) + float(phase)) * float(Amp)
        datalst.append(int(tempf))
        #print int(tempf)
        xArray = xArray + pack('h',int(tempf))
#print unpack('hhh',xArray[0:6])
print "calc finished"
print len(xArray)
#pyplot.plot(datalst)
#pyplot.show()

def callback(in_data, frame_count, time_info, status):
    data=xArray[callback.offset:frame_count*2+callback.offset]
    callback.offset = (frame_count*2+callback.offset)%(sam_rate/freq*2)
    return (data, pyaudio.paContinue)

callback.offset = 0

stream = p.open(format = format1,
                channels=channel,
                rate=rates,
                output = True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.01)

#while True:
    ##data = wf.readframes(chunk)
    #stream.write(data)
    ##xArray = cos(2.0*pi*freq*T/sam_rate + phase) * Amp
    ##data = xArray.astype(int)
    #counter = counter - 1
    #if counter == 0: break
    ##pyplot.plot(data)
    ##pyplot.show()

stream.stop_stream()
stream.close()
p.terminate()

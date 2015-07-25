# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:48:07 2015

@author: Administrator
"""

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from scipy import fftpack
from scipy import signal

RFRATE = 0.25e6
RFFREQ = 104.300e6
RFGAIN = 50

DOWN_FACTOR = 10

RFSIZE = int(512*10)
AUDIOSIZE = int(RFSIZE/DOWN_FACTOR)
data =[]
CHANNELS = 1
AUDIORATE = int(RFRATE/DOWN_FACTOR)

audata =[]


#processing block
rfwindow = signal.hamming(RFSIZE)
audiowindow = signal.hamming(AUDIOSIZE)
fftwindow = signal.hamming(512)

T=np.arange(0,RFSIZE,1)
xInput =np.cos(2*np.pi*T*(4/RFSIZE))
m=1000000
C=0
xCa=np.cos(m*xInput+2*np.pi*T*(C/RFSIZE))+1j*np.sin(m*xInput+2*np.pi*T*(C/RFSIZE))
plta = plt.subplot(4,1,1)
plta.set_title("Input")
plt.plot(xInput)
pltb = plt.subplot(4,1,2)
pltb.set_title("After Mod Real")
plt.plot(xCa.real)
pltc = plt.subplot(4,1,3)
pltc.set_title("After Mod Imag")
plt.plot(xCa.imag)

freq=fftpack.fft(xCa,xCa.size)
freq_plot=np.abs(freq)[0:freq.size/2+1]


#xCa=signal.decimate(xCa,DOWN_FACTOR,ftype="fir")

#pre_data=1
#dec_data_delay=np.insert(xCa,0,pre_data)
#pre_data = dec_data_delay[-1]
#dec_data_delay=np.delete(dec_data_delay,-1)
#diff_data=xCa*np.conj(dec_data_delay)
#audioda=np.angle(diff_data)
#audiodata=np.unwrap(audioda)

#audiodata=np.arctan2(diff_data.imag,diff_data.real)
#
angle_data=np.angle(xCa)

audioda=np.diff(angle_data)
audiodata=np.unwrap(audioda)

#
#pre_data=1
#data=xCa
#data_diff=np.insert(np.diff(data),0,pre_data)
#audiodata=data.real*data_diff.imag-data.imag*data_diff.real
#audiodata=audiodata/(np.power(data.real,2)+np.power(data.imag,2))

audiodata=signal.decimate(audiodata,DOWN_FACTOR,ftype="fir")

pltd = plt.subplot(4,1,4)
pltd.set_title("demod")
plt.plot(audiodata)
            #fft_input=data[0:AUDIOSIZE]*fftwindow
            #fft_input=audiodata*fftwindow
            #fft_data=fftpack.fftshift(fftpack.fft(fft_input,overwrite_x=True))
            #rt_input=dec_data*fftwindow
            #rt_data=fftpack.fftshift(fftpack.fft(rt_input,overwrite_x=True))
            #fft_temp_data=fftpack.fft(fft_input,overwrite_x=True)
            #fft_data=fft_data_sum/50
            #fft_data_sum=(np.abs(fft_temp_data)+fft_data_sum)-fft_data

plt.savefig('pic.png')
print('ended')

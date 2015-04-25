# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:48:07 2015

@author: Administrator
"""

import matplotlib.pyplot as plt
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
xInput =np.cos(2*np.pi*T*(2/RFSIZE))
m=10
C=0
xCa=np.cos(m*xInput+2*np.pi*T*(C/RFSIZE))+1j*np.sin(m*xInput+2*np.pi*T*(C/RFSIZE))
plt.subplot(4,1,1)
plt.plot(xInput)
plt.subplot(4,1,2)
plt.plot(xCa.real)
plt.subplot(4,1,3)
plt.plot(xCa.imag)



freq=fftpack.fft(xCa,xCa.size)
freq_plot=np.abs(freq)[0:freq.size/2+1]
#pl.subplot(4,1,3)
#plt.plot(freq_plot)




#pl.subplot(4,1,3)
#plt.plot(dec_data)
#
audiodata=signal.decimate(xCa,DOWN_FACTOR,ftype="fir")
#pre_data=1
#dec_data_delay=np.insert(xCa,0,pre_data)
#pre_data = dec_data_delay[-1]
#dec_data_delay=np.delete(dec_data_delay,-1)
#diff_data=xCa*np.conj(dec_data_delay)
#fdec_data=np.angle(diff_data)
#audiodata=np.arctan2(diff_data.imag,diff_data.real)
#
angle_data=np.angle(xCa)
angle_data=np.unwrap(angle_data)
audiodata=np.diff(angle_data)



plt.subplot(4,1,4)
plt.plot(audiodata)
            #fft_input=data[0:AUDIOSIZE]*fftwindow
            #fft_input=audiodata*fftwindow
            #fft_data=fftpack.fftshift(fftpack.fft(fft_input,overwrite_x=True))
            #rt_input=dec_data*fftwindow
            #rt_data=fftpack.fftshift(fftpack.fft(rt_input,overwrite_x=True))
            #fft_temp_data=fftpack.fft(fft_input,overwrite_x=True)
            #fft_data=fft_data_sum/50
            #fft_data_sum=(np.abs(fft_temp_data)+fft_data_sum)-fft_data


print('ended')

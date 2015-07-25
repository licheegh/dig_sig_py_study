# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:48:07 2015

@author: Administrator
"""

import tkinter as tk
import multiprocessing
import numpy as np
from scipy import fftpack
from scipy import signal
from rtlsdr import *
import pyaudio
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

RFRATE = 0.25e6
RFFREQ = 103.5e6
RFGAIN = 50

DOWN_FACTOR = 10

RFSIZE = int(512*10)
AUDIOSIZE = int(RFSIZE/DOWN_FACTOR)
FORMAT = pyaudio.paInt16
CHANNELS = 1
AUDIORATE = int(RFRATE/DOWN_FACTOR)

tempdata = np.zeros(AUDIOSIZE)


if __name__ == '__main__':
    data=np.load("data.npy")
#    data = np.ones(16,np.complex)
    #half= np.power(2,.5)/2
#    half= 1
#    data[0] = 1
#    data[1] = half+half*1j
#    data[2] = 1j
#    data[3] = -half+half*1j
#    data[4] = -1
#    data[5] = -half-half*1j
#    data[6] = -1j
#    data[7] = half-half*1j
#    data[8] = 1
#    data[9] = half+half*1j
#    data[10] = 1j
#    data[11] = -half+half*1j
#    data[12] = -3
#    data[13] = -half-half*1j
#    data[14] = -5j
#    data[15] = half-half*1j
#    
#    ticks = np.linspace(0,np.pi*2,5)
#    imag=np.cos(ticks)
#    real=np.sin(ticks)*1j
#    data = real+imag
    
    diff = np.ones(3)
    diff[0] = .5
    diff[1] = 0
    diff[2] = -.5

#    diff = np.ones(5)
#    diff[0] = -1/6
#    diff[1] = 8/6
#    diff[2] = 0
#    diff[3] = -8/6
#    diff[4] = 1/6
    

    pre_data1=0
    #demod method 1
    angle_data=np.angle(data)
    audioda=np.diff(angle_data)
    audiodata1=np.insert(audioda,0,angle_data[0]-pre_data1)
    pre_data1=angle_data[-1]
    audiodata1=np.unwrap(audiodata1,np.pi)
    #audiodata1=audioda
    #audiodata1=np.unwrap(audiodata1,np.pi)
    
    pre_data2=0
    #demod method 2
    data_delay=np.insert(data,0,pre_data2)
    pre_data2 = data_delay[-1]
    data_delay=np.delete(data_delay,-1)
    diff_data2=data*np.conj(data_delay)
    audiodata2=np.angle(diff_data2)
    #audiodata2=np.unwrap(audiodata2)


    pre_data3=0
    #demod method 3
    diff_data_pre = signal.convolve(diff, data)
    data_dly1=np.delete(data,0)
    diff_data3=diff_data_pre[2:]
    diff_data3=np.delete(diff_data3,diff_data3.size-1)
    #data=np.delete(data,data.size-1)
    #data=np.delete(data,0)
    #data=np.delete(data,0)
    #data=np.insert(data,0,1-1j)
    #diff_data=np.insert(diff_data,diff_data.size,data[0]-pre_data3)
    #pre_data3=data[-1]
    audiodata3=data_dly1.real*diff_data3.imag-data_dly1.imag*diff_data3.real
    audiodata3=audiodata3/(np.power(data_dly1.real,2)+np.power(data_dly1.imag,2))
  
#  audiodata=audiodata*10    
    
    #demod method 4
    diff_data4=np.diff(data)
    #data_dly=np.delete(data,0)
    #data_dly=np.delete(data,0)
    data_dly2=np.delete(data,0)
    #diff_data=diff_data_pre[2:]
    #diff_data=np.delete(diff_data,diff_data.size-1)
    #data=np.delete(data,data.size-1)
    #data=np.delete(data,0)
    #data=np.delete(data,0)
    #data=np.insert(data,0,1-1j)
    #diff_data=np.insert(diff_data,diff_data.size,data[0]-pre_data3)
    #pre_data3=data[-1]
    audiodata4=data_dly2.real*diff_data4.imag-data_dly2.imag*diff_data4.real
    audiodata4=audiodata4/(np.power(data_dly2.real,2)+np.power(data_dly2.imag,2))
    
    #audiodata=signal.decimate(audiodata,DOWN_FACTOR,ftype="fir")

    #plt.plot(data.real,'b')
    #plt.plot(data.imag,'r')
    #plt.subplot(3,1,1)
    #plt.plot(audiodata,'r')
    #plt.show()
    #print(audiodata.size)
    print(audiodata1)
    print(audiodata2)
    print(audiodata3)
    print(audiodata4)
    
    #processes
    #data_pad=np.pad(data,(0,1024-data.size),'constant', constant_values=0)
    #datafft=fftpack.fft(data_pad,data_pad.size)
    datafft=fftpack.fft(data,data.size)
    datafft_abs = np.abs(datafft)

    audiodata2_fft=fftpack.fft(audiodata2,audiodata2.size)
    audiodata2_fftabs = np.abs(audiodata2_fft)
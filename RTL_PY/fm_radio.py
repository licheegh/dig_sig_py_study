# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:48:07 2015

@author: Administrator
"""

import tkinter as tk
#import threading
import multiprocessing
#import queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as line
import numpy as np
from scipy import fftpack
from scipy import signal
from rtlsdr import *
import pyaudio

RFRATE = 0.25e6
RFFREQ = 104.3e6
RFGAIN = 50

DOWN_FACTOR = 10

RFSIZE = int(512*10)
AUDIOSIZE = int(RFSIZE/DOWN_FACTOR)
FORMAT = pyaudio.paInt16
CHANNELS = 1
AUDIORATE = int(RFRATE/DOWN_FACTOR)

tempdata = np.zeros(AUDIOSIZE)

def read_data_thread(rf_q,ad_rdy_ev,audio_q):
    pre_data=0

    #while stream.is_active():
    print("read data thread start")
    while 1:
        ad_rdy_ev.wait(timeout=1000)
        while not rf_q.empty():
            #process audio data here
            data=rf_q.get()
            #print('  signal mean:', sum(data)/len(data))
            #data=signal.decimate(data,DOWN_FACTOR,ftype="fir")
            #diff_data=np.diff(dec_data)
            #audioda=np.angle(diff_data)
            #audiodata=np.insert(audioda,0,0)

            #data = signal.filtfilt(FIR_LP,1.0,data)
            #data = signal.lfilter(FIR_LP,1.0,data)

            angle_data=np.angle(data)
            audioda=np.diff(angle_data)
            audiodata=np.insert(audioda,0,angle_data[0]-pre_data)
            pre_data=angle_data[-1]
            audiodata=np.unwrap(audiodata,np.pi)


            #data_delay=np.insert(data,0,pre_data)
            #pre_data = data_delay[-1]
            #data_delay=np.delete(data_delay,-1)
            #diff_data=data*np.conj(data_delay)
            #audiodata=np.angle(diff_data)
            #audiodata=np.unwrap(audiodata)


            #diff_data=np.diff(data)
            #diff_data=np.insert(diff_data,0,data[0]-pre_data)
            #pre_data=data[-1]
            #audiodata=data.real*diff_data.imag-data.imag*diff_data.real
            #audiodata=audiodata/(np.power(data.real,2)+np.power(data.imag,2))
            #audiodata=audiodata*10


            audiodata=signal.decimate(audiodata,DOWN_FACTOR,ftype="fir")

            #audiodata = signal.lfilter(FIR_LP,1.0,audiodata)

            audiodata_amp=audiodata*1e4
            snd_data = audiodata_amp.astype(np.dtype('<i2')).tostring()
            audio_q.put(snd_data)
            #rt_data = audiodata
            #fft_input=data[0:AUDIOSIZE]*fftwindow
            #fft_input=audiodata*fftwindow
            #fft_data=fftpack.fftshift(fftpack.fft(fft_input,overwrite_x=True))
            #rt_input=dec_data*fftwindow
            #rt_data=fftpack.fftshift(fftpack.fft(rt_input,overwrite_x=True))
            #fft_temp_data=fftpack.fft(fft_input,overwrite_x=True)
            #fft_data=fft_data_sum/50
            #fft_data_sum=(np.abs(fft_temp_data)+fft_data_sum)-fft_data
        ad_rdy_ev.clear()

def rtlsdr_callback(samples, context):
    #global ad_rdy_ev
    #global rf_q

    context[1].put(samples)
    context[0].set()

def rtlsdr_thread(rf_q,ad_rdy_ev):

    print('rtlsdr thread start')
    sdr = RtlSdr()

    sdr.rs = RFRATE
    sdr.fc = RFFREQ
    sdr.gain = RFGAIN
    #sdr.freq_correction = -13read_bytes_async
    sdr.set_agc_mode(True)
    print('  sample rate: %0.6f MHz' % (sdr.rs/1e6))
    print('  center frequency %0.6f MHz' % (sdr.fc/1e6))
    print('  gain: %d dB' % sdr.gain)
    #ad_rdy_ev.set()
    #rf_q.put([1,2,3])
    context=[ad_rdy_ev,rf_q]
    sdr.read_samples_async(rtlsdr_callback, RFSIZE,context)
    #while 1:
        #data = sdr.read_samples(RFSIZE)
        #rf_q.put(data)
        #ad_rdy_ev.set()
    print('read rtlsdr thread ended')


zero_data = tempdata.astype(np.dtype('<i2')).tostring()
def audio_callback(in_data, frame_count, time_info, status):
    global audio_q
    global zero_data

    if not audio_q.empty():
        return (audio_q.get(),pyaudio.paContinue)
    else:
        return (zero_data,pyaudio.paContinue)



#GUI
class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.creatWidgets()

    def creatWidgets(self):
        self.quitButton=tk.Button(self,text='quit',command=root.destroy)
        self.quitButton.grid(column=1,row=3)

def plot_init():
    rt_ax.add_line(rt_line)
    fft_ax.add_line(fft_line)
    return fft_line,rt_line,
    
def plot_update(i):
    global rt_data
    global fft_data
    
    rt_line.set_xdata(rt_x_data)
    rt_line.set_ydata(rt_data)
    
    fft_line.set_xdata(fft_x_data)
    fft_line.set_ydata(fft_data)
    return fft_line,rt_line,


if __name__ == '__main__':
    global sdr
    rf_q = multiprocessing.Queue()
    audio_q = multiprocessing.Queue()

    ad_rdy_ev=multiprocessing.Event()

    #audata =[]


    #filter design
    #FIR_LP = signal.firwin(19,17e3,1e3,window='hamming',True,False,RFRATE/2)
    #FIR_LP = signal.firwin(19,400e3/(RFRATE/2))
    #FIR_LP = signal.firwin(9,10e3/(AUDIORATE/2))

    #Matplotlib
    fig = plt.figure()
    rt_ax = plt.subplot(212,xlim=(0,AUDIOSIZE), ylim=(-5,5))
    #rt_ax = plt.subplot(212,xlim=(0,AUDIOSIZE), ylim=(0.01,100))
    fft_ax = plt.subplot(211)
    #fft_ax.set_yscale('log')
    fft_ax.set_xlim(0,AUDIOSIZE)
    fft_ax.set_ylim(0.01,100)
    rt_ax.set_title("Real Time")
    fft_ax.set_title("FFT Time")
    rt_line = line.Line2D([],[])
    fft_line = line.Line2D([],[])
    fft_ax.set_xticks(np.arange(0,AUDIOSIZE,32))
    fftxlabels = ['%d' % i for i in np.arange(-AUDIOSIZE/2,AUDIOSIZE/2,32)*RFRATE/AUDIOSIZE/1000]
    fft_ax.set_xticklabels(fftxlabels,rotation=40)

    rt_data=np.arange(0,AUDIOSIZE,1)
    fft_data=np.arange(0,AUDIOSIZE,1)
    fft_data_sum=np.arange(0,AUDIOSIZE,1)
    rt_x_data=np.arange(0,AUDIOSIZE,1)
    fft_x_data=np.arange(0,AUDIOSIZE,1)


    #ani = animation.FuncAnimation(fig, plot_update,
                                  #init_func=plot_init, 
                                  #frames=1,
                                  #interval=30,
                                  #blit=True)
    #pyaduio
    p = pyaudio.PyAudio()
    print("SoundCard Output @ %d KHz" % (AUDIORATE/1e3))
    stream = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=AUDIORATE,
            input=False,
            output=True,
            frames_per_buffer=AUDIOSIZE,
            stream_callback=audio_callback)
    stream.start_stream()

    #rtlsdr

    #processing block
    rfwindow = signal.hamming(RFSIZE)
    audiowindow = signal.hamming(AUDIOSIZE)
    fftwindow = signal.hamming(512)

        
        
    t_read_data=multiprocessing.Process(target=read_data_thread,args=(rf_q,ad_rdy_ev,audio_q,))
    #t_read_data=multiprocessing.Process(target=read_data_thread)
    t_rtlsdr=multiprocessing.Process(target=rtlsdr_thread,args=(rf_q,ad_rdy_ev,))

    print("Start thread")

    t_read_data.daemon=True
    t_read_data.start()
    t_rtlsdr.daemon=True
    t_rtlsdr.start()


    #plt.show()
    root=tk.Tk()
    app=Application(master=root)
    app.master.title("Test")
    app.mainloop()

    stream.stop_stream()
    stream.close()
    sdr.cancel_read_async()
    sdr.close()
    #np.savetxt("audioda.txt",audioda,"%10.5f")
    #np.savetxt("dec_data.txt",dec_data,"%10.5f")
    #np.savetxt("data.txt",data,"%10.5f %10.5fi")
    #np.savetxt("angle_data.txt",angle_data,"%10.5f")
    #np.savetxt("audiodata.txt",audiodata,"%10.5f")

    

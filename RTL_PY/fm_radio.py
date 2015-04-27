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

RFRATE = 0.25e6
RFFREQ = 89.8e6
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
    #filter design
    #FIR_LP = signal.firwin(19,17e3,1e3,window='hamming',True,False,RFRATE/2)
    #FIR_LP = signal.firwin(19,400e3/(RFRATE/2))
    #FIR_LP = signal.firwin(9,10e3/(AUDIORATE/2))
    rfwindow = signal.hamming(RFSIZE)
    audiowindow = signal.hamming(AUDIOSIZE)
    fftwindow = signal.hamming(512)

    print("read data thread start")
    while 1:
        ad_rdy_ev.wait(timeout=1000)
        while not rf_q.empty():
            #process data here
            data=rf_q.get()
            #data=signal.decimate(data,DOWN_FACTOR,ftype="fir")

            #data = signal.lfilter(FIR_LP,1.0,data)

            #demod method 1
            #angle_data=np.angle(data)
            #audioda=np.diff(angle_data)
            #audiodata=np.insert(audioda,0,angle_data[0]-pre_data)
            #pre_data=angle_data[-1]
            #audiodata=np.unwrap(audiodata,np.pi)


            #demod method 2
            #data_delay=np.insert(data,0,pre_data)
            #pre_data = data_delay[-1]
            #data_delay=np.delete(data_delay,-1)
            #diff_data=data*np.conj(data_delay)
            #audiodata=np.angle(diff_data)
            #audiodata=np.unwrap(audiodata)


            #demod method 3
            diff_data=np.diff(data)
            diff_data=np.insert(diff_data,0,data[0]-pre_data)
            pre_data=data[-1]
            audiodata=data.real*diff_data.imag-data.imag*diff_data.real
            #audiodata=audiodata/(np.power(data.real,2)+np.power(data.imag,2))
            audiodata=audiodata*10

            audiodata=signal.decimate(audiodata,DOWN_FACTOR,ftype="fir")

            #audiodata = signal.lfilter(FIR_LP,1.0,audiodata)

            audiodata_amp=audiodata*1e4
            snd_data = audiodata_amp.astype(np.dtype('<i2')).tostring()
            audio_q.put(snd_data)
        ad_rdy_ev.clear()

#rtlsdr
def rtlsdr_callback(samples, context):

    context[1].put(samples)
    context[0].set()

def rtlsdr_thread(rf_q,ad_rdy_ev):

    print('rtlsdr thread start')
    sdr = RtlSdr()
    sdr.rs = RFRATE
    sdr.fc = RFFREQ
    sdr.gain = RFGAIN
    #sdr.freq_correction = -13
    sdr.set_agc_mode(True)
    print('  sample rate: %0.6f MHz' % (sdr.rs/1e6))
    print('  center frequency %0.6f MHz' % (sdr.fc/1e6))
    print('  gain: %d dB' % sdr.gain)
    context=[ad_rdy_ev,rf_q]
    sdr.read_samples_async(rtlsdr_callback, RFSIZE,context)
    sdr.cancel_read_async()
    sdr.close()
    print('read rtlsdr thread ended')


#audio call back
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

if __name__ == '__main__':
    global sdr

    #processes
    rf_q = multiprocessing.Queue()
    audio_q = multiprocessing.Queue()
    ad_rdy_ev=multiprocessing.Event()

    t_read_data=multiprocessing.Process(target=read_data_thread,args=(rf_q,ad_rdy_ev,audio_q,))
    t_rtlsdr=multiprocessing.Process(target=rtlsdr_thread,args=(rf_q,ad_rdy_ev,))

    t_read_data.daemon=True
    t_read_data.start()
    t_rtlsdr.daemon=True
    t_rtlsdr.start()

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

    root=tk.Tk()
    app=Application(master=root)
    app.master.title("Test")
    app.mainloop()

    stream.stop_stream()
    stream.close()

    

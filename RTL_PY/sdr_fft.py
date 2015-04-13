# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:48:07 2015

@author: Administrator
"""

import tkinter as tk
import threading
import queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as line
import numpy as np
from scipy import fftpack
from scipy import signal
from rtlsdr import *

SIZE = 1024
data =[]
ad_rdy_ev=threading.Event()

#GUI
class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.creatWidgets()

    def creatWidgets(self):
        self.quitButton=tk.Button(self,text='quit',command=root.destroy)
        self.quitButton.grid(column=1,row=3)


#Matplotlib
fig = plt.figure()
rt_ax = plt.subplot(212,xlim=(0,SIZE), ylim=(-0.5,0.5))
fft_ax = plt.subplot(211)
fft_ax.set_yscale('log')
fft_ax.set_xlim(0,SIZE)
fft_ax.set_ylim(0.01,100)
rt_ax.set_title("Real Time")
fft_ax.set_title("FFT Time")
rt_line = line.Line2D([],[])
fft_line = line.Line2D([],[])

rt_data=np.arange(0,SIZE,1)
fft_data=np.arange(0,SIZE,1)
rt_x_data=np.arange(0,SIZE,1)
fft_x_data=np.arange(0,SIZE,1)

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


ani = animation.FuncAnimation(fig, plot_update,
                              init_func=plot_init, 
                              frames=1,
                              interval=30,
                              blit=True)


q = queue.Queue()

#rtlsdr
sdr = RtlSdr()

#processing block
window = signal.hamming(SIZE)

def read_data_thread(q,ad_rdy_ev):
    global rt_data,fft_data

    #while stream.is_active():
    while 1:
        ad_rdy_ev.wait(timeout=1000)
        if not q.empty():
            #process audio data here
            data=q.get()
            #print('  signal mean:', sum(data)/len(data))
            while not q.empty():
                q.get()
            rt_data = np.real(data)
            #rt_data = np.frombuffer(data,np.dtype('<i2'))
            data = data * window
            fft_temp_data=fftpack.fft(data,overwrite_x=True)
            fft_data=np.abs(fft_temp_data)[0:fft_temp_data.size]
            #if Recording :
                #frames.append(data)
        ad_rdy_ev.clear()

#@limit_calls(3)
def rtlsdr_callback(samples, rtlsdr_obj):
    global ad_rdy_ev
    global q

    q.put(samples)
    ad_rdy_ev.set()

def rtlsdr_thread():
    global sdr

    print('Configuring SDR...')
    sdr.rs = 1e6
    sdr.fc = 89.7e6
    sdr.gain = 50
    print('  sample rate: %0.6f MHz' % (sdr.rs/1e6))
    print('  center frequency %0.6f MHz' % (sdr.fc/1e6))
    print('  gain: %d dB' % sdr.gain)
    sdr.read_samples_async(rtlsdr_callback, 1*1024)
    print('read rtlsdr thread ended')
    
    
t_read_data=threading.Thread(target=read_data_thread,args=(q,ad_rdy_ev))
t_rtlsdr=threading.Thread(target=rtlsdr_thread)

print("Start thread")

#t_read_data.daemon=True
t_read_data.start()
#t_rtlsdr.daemon=True
t_rtlsdr.start()


plt.show()
root=tk.Tk()
app=Application(master=root)
app.master.title("Test")
app.mainloop()

sdr.cancel_read_async()
sdr.close()

print('ended')

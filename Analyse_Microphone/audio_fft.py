# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:48:07 2015

@author: Administrator
"""

import pyaudio
import tkinter as tk
import wave
import threading
import queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as line
import numpy as np
from scipy import fftpack
from scipy import signal

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
data =[]
Recording=False
FFT_LEN = 128
frames=[]
counter=1

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
rt_ax = plt.subplot(212,xlim=(0,CHUNK), ylim=(-10000,10000))
fft_ax = plt.subplot(211)
fft_ax.set_yscale('log')
fft_ax.set_xlim(0,CHUNK/2 + 1)
fft_ax.set_ylim(1,100000000)
rt_ax.set_title("Real Time")
fft_ax.set_title("FFT Time")
rt_line = line.Line2D([],[])
fft_line = line.Line2D([],[])

rt_data=np.arange(0,CHUNK,1)
fft_data=np.arange(0,CHUNK/2 + 1,1)
rt_x_data=np.arange(0,CHUNK,1)
fft_x_data=np.arange(0,CHUNK/2 + 1,1)

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


# pyaudio
p = pyaudio.PyAudio()
q = queue.Queue()

def audio_callback(in_data, frame_count, time_info, status):
    global data    
    q.put(in_data)
    #data=in_data
    global ad_rdy_ev
    ad_rdy_ev.set()
    if counter <= 0:
        return (None,pyaudio.paComplete)
    else:
        return (None,pyaudio.paContinue)


stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=False,
        frames_per_buffer=CHUNK,
        stream_callback=audio_callback)


if Recording:
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

print("Start Recording")
stream.start_stream()

#processing block

window = signal.hamming(CHUNK)

def read_audio_thead(q,stream,frames,ad_rdy_ev):
    global rt_data
    global fft_data

    while stream.is_active():
        ad_rdy_ev.wait(timeout=1000)
        if not q.empty():
            #process audio data here
            data=q.get()
            while not q.empty():
                q.get()
            rt_data = np.frombuffer(data,np.dtype('<i2'))
            rt_data = rt_data * window
            fft_temp_data=fftpack.fft(rt_data,rt_data.size,overwrite_x=True)
            fft_data=np.abs(fft_temp_data)[0:fft_temp_data.size/2+1]
            if Recording :
                frames.append(data)
        ad_rdy_ev.clear()

ad_rdy_ev=threading.Event()

t=threading.Thread(target=read_audio_thead,args=(q,stream,frames,ad_rdy_ev))

t.daemon=True
t.start()

plt.show()
root=tk.Tk()
app=Application(master=root)
app.master.title("Test")
app.mainloop()

stream.stop_stream()
stream.close()
p.terminate()

print("* done recording")
if Recording:
    wf.writeframes(b''.join(frames))
    wf.close()


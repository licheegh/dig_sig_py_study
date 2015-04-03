# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:48:07 2015

@author: Administrator
"""

import pyaudio
import tkinter as tk
import wave
from time import sleep
import threading
import queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as line
import numpy as np

def calculate():
    global counter
    counter=-1
    print('change')

class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.grid()
        self.creatWidgets()


    def creatWidgets(self):
        #value_entered=tk.StringVar()

        self.quitButton=tk.Button(self,text='quit',command=root.destroy)
        self.quitButton.grid(column=1,row=3)

        #self.valueEntry=tk.Entry(self,width=10,textvariable=value_entered)
        #self.valueEntry.grid(column=1,row=2)

        self.funButton=tk.Button(self,text='calculate',command=calculate)
        self.funButton.grid(column=2,row=2)

        self.outputLabel=tk.Label(self,height=10,width=25,text='calculater for mm-mil')
        self.outputLabel.grid(column=1,row=1)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
data =[]

fig = plt.figure()
ax = plt.axes(xlim=(0,1024), ylim=(-10000,10000))
linem = line.Line2D([],[])

def init():
    ax.add_line(linem)
    return linem,
    
def update(i):
    linem.set_xdata(np.arange(0,1024,1))
    linem.set_ydata(np.frombuffer(data,np.dtype('<i2')))
    return linem,


#def data_gen():
#    while True: yield np.random.rand(10)

ani = animation.FuncAnimation(fig, update,
                              init_func=init, 
                              frames=1,
                              interval=30,
                              blit=True)
plt.show()

p = pyaudio.PyAudio()
q = queue.Queue()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    global data    
    q.put(in_data)
    data=in_data
    global ad_rdy_ev
    ad_rdy_ev.set()
    if counter <= 0:
        return (None,pyaudio.paComplete)
    else:
        return (None,pyaudio.paContinue)


# open stream using callback (3)
stream = p.open(format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        output=False,
        frames_per_buffer=CHUNK,
        stream_callback=callback)


wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)

print("* recording")
stream.start_stream()

frames=[]
counter=250


def read_audio_thead(q,stream,frames,ad_rdy_ev):
    while stream.is_active():
        ad_rdy_ev.wait(timeout=1)
        if not q.empty():
            frames.append(q.get())
        ad_rdy_ev.clear()

ad_rdy_ev=threading.Event()

t=threading.Thread(target=read_audio_thead,args=(q,stream,frames,ad_rdy_ev))

t.daemon=True
t.start()

root=tk.Tk()
app=Application(master=root)
app.master.title("Test")
app.mainloop()

stream.stop_stream()
stream.close()
p.terminate()

print("* done recording")
wf.writeframes(b''.join(frames))
wf.close()

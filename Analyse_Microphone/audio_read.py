# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:48:07 2015

@author: Administrator
"""

import pyaudio
import wave
import threading
import queue
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"
data =[]

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

stream.stop_stream()
stream.close()
p.terminate()

print("* done recording")
wf.writeframes(b''.join(frames))
wf.close()

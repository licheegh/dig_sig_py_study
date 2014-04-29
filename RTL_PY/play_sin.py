# -*- coding: utf-8 -*-
import pyaudio
from time import sleep
from struct import *
from math import pi,sin

class GenSin:
    def __init__(self):
        self.sample_rate=44100
        self.frequence=100
        self.amplitude=32000
        self.time_lst=range(0,self.sample_rate/self.frequence,1)
        self.phase=0
        self.data_generated = 0
        self.offset=0
        self.data_str=""
        self.data_lst=[]
    def GetData(self,data_length):
        if self.data_generated == 0:
            if data_length > self.sample_rate/self.frequence:
                self.num_copy = data_length/(self.sample_rate/self.frequence) + 1
            else:
                self.num_copy = 1
            for j in range(self.num_copy):
                for i in self.time_lst:
                    tempf=sin(2.0*pi*float(self.frequence)*float(i)/float(self.sample_rate) + float(self.phase)) * float(self.amplitude)
                    self.data_lst.append(int(tempf))
                    self.data_str = self.data_str + pack('h',int(tempf))
            self.data_generated = 1

        data=self.data_str[self.offset:data_length+self.offset]
        self.offset = (data_length+self.offset)%(self.sample_rate/self.frequence*2)
        return data

gensin=GenSin()
p = pyaudio.PyAudio()

channel = 1
rates = int(gensin.sample_rate)
audio_format = pyaudio.paInt16

def callback(in_data, frame_count, time_info, status):
    data = gensin.GetData(frame_count*2)
    return (data, pyaudio.paContinue)

stream = p.open(format = audio_format,
                channels=channel,
                rate=rates,
                output = True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    sleep(0.1)

stream.stop_stream()
stream.close()
p.terminate()

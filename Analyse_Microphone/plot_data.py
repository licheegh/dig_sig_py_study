# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pylab as pl
from scipy import fftpack

length=64
cycles=3.4
data=np.arange(0,length,1)


data=np.sin(2*np.pi*data*(cycles/data.size))


freq=fftpack.fft(data,length)
freq_plot=np.abs(freq)[0:freq.size/2+1]

#plotting
pl.subplot(1,2,1)
pl.plot(data)
pl.subplot(1,2,2)
pl.plot(freq_plot)

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 16:48:33 2015

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 10:48:07 2015

@author: Administrator
"""

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from scipy import fftpack
from scipy import signal

coeff = np.ones(2)*0.5
coeff[0] = 1
coeff[1] = -1
#coeff[2] = -1

#plt.magnitude_spectrum(coeff,window=mlab.window_none,pad_to=64,sides='default')

coeff_pad = np.pad(coeff,(0,64-coeff.size),'constant', constant_values=0)

freq=fftpack.fft(coeff_pad,coeff_pad.size)
freq_abs = np.abs(freq)
plt.subplot(2,1,1)
plt.plot(freq_abs,'b.')


T=np.arange(0,64,1)
data =np.sin(2*np.pi*T*(13/T.size))
plt.subplot(2,1,2)
plt.plot(data,'b')

data_freq=fftpack.fft(data,data.size)
data_fabs=np.abs(data_freq)/max(np.abs(data_freq))
plt.subplot(2,1,1)
plt.plot(data_fabs,'r.')

data_conv=signal.fftconvolve(data,coeff)
plt.subplot(2,1,2)
plt.plot(data_conv,'r')
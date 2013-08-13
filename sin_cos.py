from numpy import sin, linspace, pi, cos
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fft, arange

def plotSpectrum(y,Fs):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y) # length of the signal
    k = arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range

    Y = fft(y)/n # fft computing and normalization
    Y = Y[range(n/2)]

    plot(frq,abs(Y),'r') # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')

Fs = 10000.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = arange(0,1,Ts) # time vector

print t

ff = 100;   # frequency of the signal
y = sin(2*pi*ff*t)
x = (0.2*cos(2*pi*2*t)+0.4) * y

subplot(3,1,1)
plot(t,y)
subplot(3,1,2)
plot(t,x)

#plot(t,y)
#xlabel('Time')
#ylabel('Amplitude')
#subplot(2,1,2)
#plotSpectrum(y,Fs)
subplot(3,1,3)
plotSpectrum(x,100)
show()


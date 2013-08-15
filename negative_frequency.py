from numpy import sin, linspace, pi, cos, exp
from pylab import plot, show, title, xlabel, ylabel, subplot, fftshift, rfft
from scipy import fft, arange

f0MHz = 5;
fsMHz = 20;
N     = 128;
T     = arange(0,N-1.0,1.0)

xReal    = cos(2*pi*f0MHz*T/fsMHz);
xComplex = exp(1j*2*pi*f0MHz*T/fsMHz);

xRealF   = (1.0/N)*fft(xReal,N); 
xComplexF = (1.0/N)*fft(xComplex,N); 

Tplot = arange(-N/2.0,N/2.0-1.0,1)
print xRealF,xComplexF,Tplot,T
#subplot(2,1,1)
#plot(Tplot*fsMHz/N,(fftshift(abs(xRealF))));
#subplot(2,1,2)
#plot(Tplot*fsMHz/N,(fftshift(abs(xComplexF))));
#show()

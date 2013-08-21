from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot, fftshift, rfft, exp, cos
from scipy import fft, arange

import file_output


f0MHz = 5.0;
f0MHzmul = 1.0;
fsMHz = 20.0;
N     = 128;
T     = arange(0.0,float(N),1.0)
MyPi  = 3.1416

xReal    = cos(2.0*MyPi*f0MHz*T/fsMHz);
xRealmul = cos(2.0*MyPi*f0MHz*T/fsMHz)*cos(2.0*MyPi*f0MHzmul*T/fsMHz)
xComplex = exp(1j*2.0*MyPi*f0MHz*T/fsMHz);
xComplexneg = exp(-1j*2.0*MyPi*f0MHz*T/fsMHz);

xRealF   = (1.0/N)*fft(xReal,N); 
xRealFmul= (1.0/N)*fft(xRealmul,N);
xComplexF = (1.0/N)*fft(xComplex,N); 
xComplexFneg = (1.0/N)*fft(xComplexneg,N); 

Tplot = arange(-N/2.0,N/2.0,1)
subplot(5,1,1)
plot(Tplot*fsMHz/N,(fftshift(abs(xRealF))));
subplot(5,1,2)
plot(Tplot*fsMHz/N,(fftshift(abs(xComplexF))));
subplot(5,1,3)
plot(Tplot*fsMHz/N,(fftshift(abs(xComplexFneg))));
subplot(5,1,4)
plot(Tplot*fsMHz/N,(fftshift(abs(xRealFmul))));
show()

f=open('output.txt','w')
file_output.comple_w(f, xReal, 'xReal')
file_output.comple_w(f, xComplex, 'xComplex')
file_output.comple_w(f, xRealF, 'xRealF')
file_output.comple_w(f, xComplexF, 'xComplexF')
f.close()

from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot, fftshift, rfft, exp, cos
from scipy import fft, arange

import file_output


fcarr	= 1.0
finput	= 0.1
fs		= 0.1
fsmod	= 20.0
N     = 4096
T     = arange(0.0,float(N),1.0)
MyPi  = pi
ModRatio = 0.5

xInput = cos(2.0*MyPi*finput*T/fsmod)
xCarrier = cos(2.0*MyPi*fcarr*T/fsmod)
xMod = (xInput * ModRatio + 1) * xCarrier

xInputF = (1.0/N)*fft(xInput,N); 
xCarrierF = (1.0/N)*fft(xCarrier,N);
xModF = (1.0/N)*fft(xMod,N); 
#xComplexFneg = (1.0/N)*fft(xComplexneg,N); 

Tplot = arange(-N/2.0,N/2.0,1)
pic_n=5
subplot(pic_n,1,1)
plot(Tplot*fsmod/N,(fftshift(abs(xModF))));
subplot(pic_n,1,2)
plot(Tplot*fsmod/N,(fftshift(abs(xCarrierF))));
subplot(pic_n,1,3)
plot(T,xInput);
subplot(pic_n,1,4)
plot(T,xMod);
subplot(pic_n,1,5)
plot(T,xCarrier);
#subplot(5,1,4)
#plot(Tplot*fsMHz/N,(fftshift(abs(xRealFmul))));
show()

#f=open('output.txt','w')
#file_output.comple_w(f, xReal, 'xReal')
#file_output.comple_w(f, xComplex, 'xComplex')
#file_output.comple_w(f, xRealF, 'xRealF')
#file_output.comple_w(f, xComplexF, 'xComplexF')
#f.close()

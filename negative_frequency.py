from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot, fftshift, rfft, exp, cos
from scipy import fft, arange

f0MHz = 5.0;
fsMHz = 20.0;
N     = 128;
T     = arange(0.0,float(N),1.0)
MyPi  = 3.1416

xReal    = cos(2.0*MyPi*f0MHz*T/fsMHz);
xComplex = exp(1j*2.0*MyPi*f0MHz*T/fsMHz);

xRealF   = (1.0/N)*rfft(xReal,N); 
xComplexF = (1.0/N)*rfft(xComplex,N); 

Tplot = arange(-N/2.0,N/2.0,1)
#print xReal
#print xComplex
#print
#print xRealF
#print xComplexF
#print Tplot
#print T
#subplot(2,1,1)
#plot(Tplot*fsMHz/N,(fftshift(abs(xRealF))));
#subplot(2,1,2)
#plot(Tplot*fsMHz/N,(fftshift(abs(xComplexF))));
#show()

f=open('output.txt','w')
f.write('\nxReal:\n')
f.write(str(xReal))
f.write('\nxComplex:\n')
f.write(str(xComplex))
f.write('\nxRealF:\n')
f.write(str(xRealF))
f.write('\nxComplexF:\n')
f.write(str(xComplexF))
f.close()

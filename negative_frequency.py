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

xRealF   = (1.0/N)*fft(xReal,N); 
xComplexF = (1.0/N)*fft(xComplex,N); 

Tplot = arange(-N/2.0,N/2.0,1)
subplot(2,1,1)
plot(Tplot*fsMHz/N,(fftshift(abs(xRealF))));
subplot(2,1,2)
plot(Tplot*fsMHz/N,(fftshift(abs(xComplexF))));
show()

f=open('output.txt','w')
f.write('xReal:\n')
for number in xReal:
	f.write(('\t{0.real:+.8e} {0.imag:+.8e}i\n').format(number))
f.write('\nxComplex:\n')
for number in xComplex:
	f.write(('\t{0.real:+.8e} {0.imag:+.8e}i\n').format(number))
f.write('\nxRealF:\n')
for number in xRealF:
	f.write(('\t{0.real:+.8e} {0.imag:+.8e}i\n').format(number))
f.write('\nxComplexF:\n')
for number in xComplexF:
	f.write(('\t{0.real:+.8e} {0.imag:+.8e}i\n').format(number))
f.close()

from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fft, arange
import numpy as np

def googleant2(real,imag):
    
    lQ=0
    lI=1
    div=0
    AMPL_CONV=1
    imag=imag.imag

    real=lI*real+lQ*imag
    imag=lI*imag-real*lQ
        
    sgn=1
    if imag<0:
        sgn *= -1
        imag *= -1
    ang=0
    if real==imag:
        div=1
    elif real>imag:
        div=imag/real
    else:
        ang = -np.pi / 2
        div = real / imag
        sgn *= -1
        
    out= sgn *(ang + div/ (0.98419158358617365+ div * (0.093485702629671305+ div * 0.19556307900617517))) * AMPL_CONV
    
    #print(out)    
    return out

def standard(real,imag):
    data=real+imag
    out = np.angle(data)
    #print(out)
    return out



data=np.empty(0)
stan=np.empty(0)
length=100
for i in range(0,length):
    ticks=(360/length*i)/180*np.pi
    #print('tick:%.1f' % (ticks/np.pi*180))
    imag=np.sin(ticks)*1j
    real=np.cos(ticks)
    #data = real+imag
    print('real+imag:%.1f+%.1fj tick:%.1f' % (real,imag.imag,ticks/np.pi*180))
    data=np.append(data,googleant2(real,imag))
    stan=np.append(stan,standard(real,imag))
    

datao=data/np.pi*180
stano=stan/np.pi*180

print('data:'+np.array_str(datao)+'\n'+'stan:'+np.array_str(stano))

plot(stano)
plot(datao)
plot(stano-datao)
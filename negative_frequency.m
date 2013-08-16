%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% All rights reserved by Krishna Pillai, http://www.dsplog.com 
% The file may not be re-distributed without explicit authorization
% from Krishna Pillai.
% Checked for proper operation with Octave Version 3.0.0
% Author	: Krishna Pillai
% Email		: krishna@dsplog.com
% Version	: 1.0
% Date		: 8 August 2008
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Matlab/Octave script for plotting the spectrum for a real 
% sinusoidal and a complex sinusoidal. To demonstrate the 
% concept of negative frequency

clear all
close all

f0MHz = 5; % signal frequency
fsMHz = 20; % sampling frequency
N     = 128; % fft size
MyPai  = 3.1416;

% generating the time domain signal
xReal    = cos(2*MyPai*f0MHz*[0:N-1]/fsMHz);
xComplex = exp(1j*2*MyPai*f0MHz*[0:N-1]/fsMHz);

% taking the FFT
xRealF   = (1/N)*fft(xReal,N); 
xComplexF = (1/N)*fft(xComplex,N); 

figure;
plot([-N/2:N/2-1]*fsMHz/N,(fftshift(abs(xRealF))));
hold on
plot([-N/2:N/2-1]*fsMHz/N,(fftshift(abs(xComplexF))),'m');
xlabel('frequency, MHz')
ylabel('amplitude')
title('frequency response of real and complex sinusoidal signal'); 
legend('real','complex');
grid on 
axis([-fsMHz/2 fsMHz/2 0 1.2])

f=fopen('matlabout.txt','wt');
fprintf(f,'xReal\n');
fprintf(f,'\t%+.8e + %+.8ei \n',[real(xReal) imag(xReal)]);
fprintf(f,'\nxComplex\n');
fprintf(f,'\t%+.8e\t\t\t%+.8ei \n',real(xComplex),imag(xComplex));
fprintf(f,'xRealF\n');
fprintf(f,'\t%+.8e\t\t\t%+.8ei \n',real(xRealF),imag(xRealF));
fprintf(f,'\nxComplexF\n');
fprintf(f,'\t%+.8e\t\t\t%+.8ei \n',real(xComplexF),imag(xComplexF));
fclose(f);



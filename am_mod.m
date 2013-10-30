%This is a AM mod test script

clear all
close all

fcarr	= 3.0;
finput	= 0.5;
finput	= 4.0;
bw = 0.01;
fs		= 0.1;
fsmod	= 20.0;
N     = 4096;
MyPi  = pi;
ModRatio = 0.5;
bwnoise = rand(size([0:N-1])).*bw - bw/2 + (ones(size([0:N-1])));
bwnoise =1;

% generating the time domain signal
xInput = cos((2.0*MyPi*(finput*bwnoise)).*[0:N-1]/fsmod);
xCarrier = cos(2.0*MyPi*fcarr*[0:N-1]/fsmod);
xMod = (xInput * ModRatio + 1) .* xCarrier;

% taking the FFT
xInputF = (1.0/N)*fft(xInput,N); 
xCarrierF = (1.0/N)*fft(xCarrier,N);
xModF = (1.0/N)*fft(xMod,N);

figure;
hold on
%plot([-N/2:N/2-1]*fsmod/N,(fftshift(abs(xInputF))),'g');
%plot([-N/2:N/2-1]*fsmod/N,(fftshift(abs(xCarrierF))),'r');
plot((-N/2:N/2-1)*fsmod/N,(fftshift(abs(xModF))),'b');
plot((-N/2:N/2-1)*fsmod/N,((xModF)),'y');
% xlabel('frequency, MHz')
% ylabel('amplitude')
% title('frequency response of real and complex sinusoidal signal'); 
%legend('xInputF','xCarrierF','xModF');
grid on
%axis([-fsmod/2 fsmod/2 0 1.2])

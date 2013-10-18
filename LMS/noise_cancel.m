clear all
close all
ratio = 3;
size = 10000;
f0MHz = 2; % signal frequency
fN1MHz = 0.1;
fN2MHz = 4;
fsMHz = 20; % sampling frequency
Noise_Level =1;
x = cos(2*pi*f0MHz*[0:size-1]/fsMHz);
n1  = Noise_Level*randn(1,size); % Observation noise signal
ratio = 10;
n2  = Noise_Level*cos(2*pi*fN1MHz*[0:size-1]/fsMHz);
ratio = 5;
n3  = Noise_Level*cos(2*pi*fN2MHz*[0:size-1]/fsMHz);
n = n1+n2+n3;
xn = x+n; % signal + noise
mu = 0.0008;            % LMS step size.
ha = adaptfilt.lms(128,mu);
[y,e] = filter(ha,n,xn);

Num_Point = 100;
subplot(2,1,1); plot(size-Num_Point:size,[e(size-Num_Point:size)],'k');
hold on
plot(size-Num_Point:size,[x(size-Num_Point:size)],'r');
%plot(xn(size-Num_Point:size),'g');
hold off
legend('filter out','org signal');
xlabel('Time Index'); ylabel('Signal Value');
subplot(2,1,2); plot(size-Num_Point:size,[xn(size-Num_Point:size);n(size-Num_Point:size)]);
%stem(ha.coefficients);
legend('sig+noi','noise');
xlabel('Coefficient #'); ylabel('Coefficient Value');
figure;
Num_Point = 1000;
subplot(2,1,1); plot(size-Num_Point:size,[e(size-Num_Point:size)],'k');
hold on
plot(size-Num_Point:size,[x(size-Num_Point:size)],'r');
%plot(xn(size-Num_Point:size),'g');
hold off
legend('filter out','org signal');
subplot(2,1,2); plot(size-Num_Point:size,[xn(size-Num_Point:size);n(size-Num_Point:size)]);
%stem(ha.coefficients);
legend('sig+noi','noise');



N = 4096;
Num_Point = 5000;
xn_fft = (1.0/N)*fft(xn(length(xn)-Num_Point:length(xn)),N); 
e_fft = (1.0/N)*fft(e(length(e)-Num_Point:length(e)),N); 
x_fft = (1.0/N)*fft(x(length(x)-Num_Point:length(x)),N); 
n_fft = (1.0/N)*fft(n(length(n)-Num_Point:length(n)),N); 
xn_fft_abs = abs(xn_fft);
e_fft_abs = abs(e_fft);
x_fft_abs = abs(x_fft);
n_fft_abs = abs(n_fft);
figure;
hold on;
subplot(3,1,1);
plot(xn_fft_abs(1:numel(xn_fft_abs)/2+1),'k');
title('signal + noise');
subplot(3,1,2);
hold on;
plot(e_fft_abs(1:numel(e_fft_abs)/2+1),'r');
plot(x_fft_abs(1:numel(x_fft_abs)/2+1),'g');
title('filted signal , signal');
subplot(3,1,3);
plot(n_fft_abs(1:numel(n_fft_abs)/2+1),'b');
title('noise');
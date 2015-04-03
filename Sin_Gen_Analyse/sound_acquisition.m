%% Data Acquisition and Analysis using MATLAB
% MATLAB supports data acquisition using the Data Acquisition Toolbox.
% This code example shows you how to easily acquire and analyze data in 
% MATLAB.  Uses MATLAB to acquire two seconds of sound data from a 
% sound card, calculate the frequency components, and plot the results.  
% See note below on how to easily update this example to use different 
% supported data acquisition hardware.
%
%% Note: Automatically generating a report in MATLAB
% Press the "Save and Publish to HTML" button in the MATLAB Editor to 
% execute this example and automatically generate a report of this work.
%
%% Step 1: Create an analog input object to communicate with data acquisition device
% In this case, a Windows sound card is used ('winsound').
ai = analoginput('winsound');
addchannel(ai,1);

%% Step 2: Configure the analog input to acquire 2 seconds of data at 8000Hz
Fs = 8000;
duration = 2;
set (ai, 'SampleRate', Fs);
set (ai, 'SamplesPerTrigger', duration*Fs);

%% Step 3: Start the acquisition and retrieve the data
start(ai);
data = getdata(ai);

%% Step 4: Determine the frequency components of the data
xfft = abs(fft(data));
mag = 20*log10(xfft);
mag = mag(1:end/2);
plot(mag);

%% Step 5: Clean up
delete(ai);
clear ai

%% Note: Using different data acquisition hardware
% The Data Acquisition Toolbox enables you to easily switch hardware
% from a sound card to another supported data acquisition device with 
% minimal changes to your MATLAB script.  This example could be repeated 
% using different hardware by simply changing two lines of code. For 
% example, if we were to use a National Instruments multifunction card 
% then we could create the analog input object using:
% ai=analoginput('nidaq',1);
% addchannel(ai,0)
%
% Likewise, if we were to use a Measurement Computing (MCC) board to 
% acquire the data, the code would read:
% ai=analoginput('mcc',8);
% addchannel(ai,1)
%
% The Data Acquisition Toolbox supports hardware from many manufacturers
% including Advantech, CONTEC, Data Translation, and others.  
% For a list of supported data acquisition hardware, visit:
% http://www.mathworks.com/products/supportedio.html?prodCode=DA
%
% To use MATLAB with instruments or serial devices, visit:
% http://www.mathworks.com/products/instrument
%
% To use MATLAB with imaging devices, visit:
% http://www.mathworks.com/products/imaq


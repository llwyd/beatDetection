import numpy as np
import scipy.io.wavfile as sw
import matplotlib.pyplot as plt
from scipy import signal

# import audio
fs,x = sw.read("audio/dancerShortmono.wav")

x = x[(fs*1):(fs*4)]

x = x / np.max(np.abs(x))

# filterbank, 6th order elliptic filter
filter_order = 6
pass_ripple = 3 #db
stop_ripple = 40 #db

filter_bank = []

sos = signal.ellip(filter_order, 3, 40, 200, output='sos', analog=False, fs=fs)
filter_bank.append(sos)

sos = signal.ellip(filter_order, 3, 40, [200, 400],btype='bandpass', output='sos', analog=False, fs=fs)
filter_bank.append(sos)

sos = signal.ellip(filter_order, 3, 40, [400, 800],btype='bandpass', output='sos', analog=False, fs=fs)
filter_bank.append(sos)

sos = signal.ellip(filter_order, 3, 40, [800, 1600],btype='bandpass', output='sos', analog=False, fs=fs)
filter_bank.append(sos)

sos = signal.ellip(filter_order, 3, 40, [1600, 3200],btype='bandpass', output='sos', analog=False, fs=fs)
filter_bank.append(sos)

sos = signal.ellip(filter_order, 3, 40, 3200,btype='highpass', output='sos', fs=fs,  analog=False)
filter_bank.append(sos)

bank0 = signal.sosfilt(filter_bank[0], x)
bank1 = signal.sosfilt(filter_bank[1], x)
bank2 = signal.sosfilt(filter_bank[2], x)
bank3 = signal.sosfilt(filter_bank[3], x)
bank4 = signal.sosfilt(filter_bank[4], x)
bank5 = signal.sosfilt(filter_bank[5], x)


plt.show();

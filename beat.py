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

# Rectify 
#bank0 = np.abs(bank0)
#bank1 = np.abs(bank1)
#bank2 = np.abs(bank2)
#bank3 = np.abs(bank3)
#bank4 = np.abs(bank4)
#bank5 = np.abs(bank5)

#half hanning window
window_length = 0.4 * fs
hanning_full = np.hanning(window_length)
hanning_size = len(hanning_full)
hanning_half = hanning_full[0:int(hanning_size/2)]
hanning_half = np.flipud(hanning_half)

hann0 = np.convolve(bank0, hanning_half,mode='same')
hann1 = np.convolve(bank1, hanning_half,mode='same')
hann2 = np.convolve(bank2, hanning_half,mode='same')
hann3 = np.convolve(bank3, hanning_half,mode='same')
hann4 = np.convolve(bank4, hanning_half,mode='same')
hann5 = np.convolve(bank5, hanning_half,mode='same')

#decimate to 210.5hz
dec0 = hann0[::200]
dec1 = hann1[::200]
dec2 = hann2[::200]
dec3 = hann3[::200]
dec4 = hann4[::200]
dec5 = hann5[::200]

# differentiator
diff0 = np.gradient(dec0)
diff1 = np.gradient(dec1)
diff2 = np.gradient(dec2)
diff3 = np.gradient(dec3)
diff4 = np.gradient(dec4)
diff5 = np.gradient(dec5)

# half wave rectify
rect0 = np.clip(diff0,0,np.max(diff0))
rect1 = np.clip(diff1,0,np.max(diff1))
rect2 = np.clip(diff2,0,np.max(diff2))
rect3 = np.clip(diff3,0,np.max(diff3))
rect4 = np.clip(diff4,0,np.max(diff4))
rect5 = np.clip(diff5,0,np.max(diff5))

plt.figure(1)
plt.subplot(2,1,1)
plt.plot(diff0)
plt.subplot(2,1,2)
plt.plot(rect0)
plt.show();

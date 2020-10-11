import numpy as np
import scipy.io.wavfile as sw
import matplotlib.pyplot as plt
from scipy import signal

# import audio
fs,x = sw.read("audio/dancerShortmono.wav")
#fs,x = sw.read("audio/hh170.wav")

x = x[(fs*4):(fs*12)]

x = x / np.max(np.abs(x))

length = len(x)

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
dec_rate = 200

dec0 = hann0[::dec_rate]
dec1 = hann1[::dec_rate]
dec2 = hann2[::dec_rate]
dec3 = hann3[::dec_rate]
dec4 = hann4[::dec_rate]
dec5 = hann5[::dec_rate]

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

#rect0 = np.abs(diff0)
#rect1 = np.abs(diff1)
#rect2 = np.abs(diff2)
#rect3 = np.abs(diff3)
#rect4 = np.abs(diff4)
#rect5 = np.abs(diff5)

# comb filter bank
tempo=[60,70,80,90,100,110,120,130,140,150,160,170,180];


dec_fs = fs / dec_rate;

comb_out0 = np.zeros([len(tempo),len(rect0)])
comb_out1 = np.zeros([len(tempo),len(rect0)])
comb_out2 = np.zeros([len(tempo),len(rect0)])
comb_out3 = np.zeros([len(tempo),len(rect0)])
comb_out4 = np.zeros([len(tempo),len(rect0)])
comb_out5 = np.zeros([len(tempo),len(rect0)])

total = np.zeros(len(tempo))

#rect0 = signal.unit_impulse(len(rect0))

b = 0.5

for i in range(len(tempo)):
	delay = int(dec_fs*(60/tempo[i]))
	print("Delay at " + str(tempo[i]) +" bpm: " + str(delay))
	# comb filter
	for j in range(len(rect0)):
		if( j < delay ):
			comb_out0[i][j]	= rect0[j]
			comb_out1[i][j]	= rect1[j]
			comb_out2[i][j]	= rect2[j]
			comb_out3[i][j]	= rect3[j]
			comb_out4[i][j]	= rect4[j]
			comb_out5[i][j]	= rect5[j]
		else:
			b = np.power(0.5, j/delay)
			comb_out0[i][j] = rect0[j] + ((1-b)*comb_out0[i][j-delay])
			comb_out1[i][j] = rect1[j] + ((1-b)*comb_out1[i][j-delay])
			comb_out2[i][j] = rect2[j] + ((1-b)*comb_out2[i][j-delay])
			comb_out3[i][j] = rect3[j] + ((1-b)*comb_out3[i][j-delay])
			comb_out4[i][j] = rect4[j] + ((1-b)*comb_out4[i][j-delay])
			comb_out5[i][j] = rect5[j] + ((1-b)*comb_out5[i][j-delay])
	total[i] = np.sum(comb_out0[i]) + np.sum(comb_out1[i]) + np.sum(comb_out2) + np.sum(comb_out3[i]) + np.sum(comb_out4[i]) + np.sum(comb_out5[i]) 

	print(total[i])


plt.figure(1)
plt.subplot(2,1,1)
plt.plot(diff0)
plt.subplot(2,1,2)
plt.plot(comb_out5[0])
plt.plot(comb_out4[5])
plt.show();

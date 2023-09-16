import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft, fftfreq

SAVE = False
AUDIO_FILEPATH = sys.argv[1]

sample_freq, audio = read(AUDIO_FILEPATH)
n = len(audio)

duration = -1  # set amount of data (in seconds) to plot. -1 mean use all data
if duration != -1:
    n = int(sample_freq * duration)
    audio = audio[:n]

# apply fast fourier transformation
yf = fft(audio)
# since the fourier trans. returns complex numbers, calculate the magnitude
yf_mag = np.abs(yf)
# the max freq will be Nyquist frequency i.e. sample_freq/2
xf = fftfreq(n, 1 / sample_freq)

plt.title(f"Frequency Domain")
plt.ylabel(f"FFT Amplitude")
plt.xlabel("Frequency (Hz)")

# because of the conjugate similarity, you can also just plot the positive domain for the x-axis
# plt.xlim(0, int(sample_freq/2))

plt.plot(xf, yf_mag)
plt.grid()

if SAVE:
    plt.savefig('../images/frequency_domain_full.png')
plt.show()
print("completed")

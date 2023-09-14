import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft, fftfreq

AUDIO_FILEPATH = sys.argv[1]

DURATION = 100 # sec
SAMPLE_RATE = 48000     # Hz
N = SAMPLE_RATE * DURATION

# read audio
sample_freq, audio = read(AUDIO_FILEPATH)  # sample_freq = no. of samples per second (Hz), len(audio) = no. data points
audio = audio[:N]

normalized_audio = audio / max(audio)


# fq vs time domain plot
# plt.plot(range(len(audio)), normalized_audio)

# fourier transformation
yf = fft(normalized_audio)
xf = fftfreq(N, 1 / SAMPLE_RATE)
# amp vs fq plot
plt.plot(xf, np.abs(yf))


# plt.axis('off')
# plt.tight_layout()  # fill space
plt.show()

print("completed")

# https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_bar.html
# TODO - create 1 img per min. Org in arc going up for 9 mins then down. Each img had diff colour like sunsrise and sunset
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.io.wavfile import read

from stack_plot import get_color_gradient  # todo cleanup
from utils.preprocess_audio import complex2polar

AUDIO_FILEPATH = sys.argv[1]
SAVE = False
USE_FULL_AUDIO = True

SAMPLE_RATE = 48000     # Hz
N = 150 # SAMPLE_RATE * DURATION
EPS = np.finfo(np.float32).eps

color_1 = "#8d7ed8"
color_2 = "#5bffef"
colours = get_color_gradient(color_1, color_2, N)


# read audio
sample_freq, audio = read(AUDIO_FILEPATH)  # sample_freq = no. of samples per second (Hz), len(audio) = no. data points
# audio = audio[:N]

# keep dropping every other column to sparsify data - it's crude but it works
while len(audio) > N:
    audio = np.delete(audio, list(range(0, len(audio), 2)), axis=0)
print("Audio with every nth col deleted: ", audio.shape)

normalized_audio = audio / max(audio)


# fq vs time domain plot
# plt.plot(range(len(audio)), normalized_audio)

# fourier transformation
yf = fft(normalized_audio)
# xf = fftfreq(N, 1 / SAMPLE_RATE)
# plt.plot(xf, np.abs(yf))

# complex to polar
radii, theta = complex2polar(yf)
ax = plt.subplot(projection='polar')
# time = bar width and colour
ax.bar(theta, radii, width=np.linspace(np.pi/32, np.pi/8, len(theta)),
       bottom=0.0, color=colours, alpha=0.4, align='center', log=False)

plt.axis('off')
plt.tight_layout()  # fill space

if SAVE:
    plt.savefig('../images/polar_bar_chart.png', transparent=True)
    print("saved")

plt.show()

print("completed")

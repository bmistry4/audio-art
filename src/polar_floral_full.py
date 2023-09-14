import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.io.wavfile import read

from utils.plot_utils import get_color_gradient, plot_patches
from utils.preprocess_audio import sparsify_audio, convert_to_bins, complex2polar, normalize_complex_coords

AUDIO_FILEPATH = sys.argv[1]
SAVE = False
USE_FULL_AUDIO = True

NUM_BINS = 10  # todo or 16
N_PER_BIN = 50  # todo or 35
bin_colours = [["#ee2ad6", "#f8f242"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]]
# bin_colours = [["#de4747", "#df3c4e"], ["#df2f55", "#df205e"], ["#dd0b67", "#da0070"], ["#d5007a", "#cf0085"],
#                 ["#c7008f", "#bd009a"], ["#b100a5", "#a301b0"], ["#9118bb", "#7b26c5"], ["#5e30ce", "#0012ff"] ]


# read audio
_, audio = read(AUDIO_FILEPATH)  # sample_freq = no. of samples per second (Hz), len(audio) = no. data points
audio = convert_to_bins(audio, NUM_BINS)
audio = sparsify_audio(audio, N_PER_BIN)

# fourier transformation
yf = fft(audio, axis=-1)

# Normalize the complex numbers
yf = normalize_complex_coords(yf)

# Create a polar plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')

for i in range(NUM_BINS):
    # complex to polar
    radii_i, theta_i = complex2polar(yf[i])
    widths_i = np.linspace(np.pi / 32, np.pi / 8, len(theta_i))
    colours_i = get_color_gradient(bin_colours[i % len(bin_colours)][0],
                                   bin_colours[i % len(bin_colours)][1],
                                   len(yf[i])
                                   )
    plot_patches(theta_i, radii_i, widths_i, colours_i, ax, radii_offset=i / NUM_BINS,
                 alphas=[1 - i / NUM_BINS] * len(theta_i))

plt.axis('off')
plt.tight_layout()  # fill space

if SAVE:
    plt.savefig('../images/polar_pretty.png', transparent=True)
    print("saved")

plt.show()

# with and without norm
# with and without radii_offset in plot_patches

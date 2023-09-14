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

NUM_BINS = 16  # todo or 16
SAMPLE_RATE = 48000  # Hz
N_PER_BIN = 500  # todo or 35 # SAMPLE_RATE * DURATION
# bin_colours = [["#ff0000", "#f9a301"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]]
# bin_colours = [["#de4747", "#df3c4e"], ["#df2f55", "#df205e"], ["#dd0b67", "#da0070"], ["#d5007a", "#cf0085"],
#                 ["#c7008f", "#bd009a"], ["#b100a5", "#a301b0"], ["#9118bb", "#7b26c5"], ["#5e30ce", "#0012ff"] ]
bin_colours = [["#ff0000", "#ff000f", ],
               ["#ff001a", "#ff0023", ],
               ["#ff002b", "#ff0032", ],
               ["#ff0039", "#ff0041", ],
               ["#ff0048", "#ff004f", ],
               ["#ff0057", "#ff005e", ],
               ["#ff0066", "#ff006e", ],
               ["#ff0076", "#fc007e", ],
               ["#f80086", "#f3008f", ],
               ["#ee0097", "#e800a0", ],
               ["#e100a8", "#d900b1", ],
               ["#d000ba", "#c700c2", ],
               ["#bc00ca", "#b000d3", ],
               ["#a200db", "#9300e3", ],
               ["#8100ea", "#6a00f1", ],
               ["#4c00f8", "#0012ff"]]

# read audio
_, audio = read(AUDIO_FILEPATH)  # sample_freq = no. of samples per second (Hz), len(audio) = no. data points
audio = convert_to_bins(audio, NUM_BINS)
audio = sparsify_audio(audio, N_PER_BIN)

# fourier transformation
yf = fft(audio, axis=-1)

# Normalize the complex numbers
yf = normalize_complex_coords(yf)
# rescale for max is 1
yf = 1 / np.max(yf, axis=-1, keepdims=True) * yf
# Create a polar plot
fig = plt.figure(figsize=(10, 10))  # todo arc use 8,4,

# plot organisation
center_x, center_y = 0.5, 0.5
fig_radius = 0.4
angles = np.linspace(0, np.pi * 2, NUM_BINS, endpoint=False)  # circle
# angles = np.linspace(0,  np.pi + (np.pi/NUM_BINS), NUM_BINS, endpoint=False) # arc

for i in range(NUM_BINS):
    # plot location = how far in audio
    # radii = as normal
    # theta = full circle (anticlockwise) represents how far in audio for segment

    # complex to polar
    radii_i, _ = complex2polar(yf[i])
    theta_i = np.linspace(0, 2 * np.pi, len(radii_i))
    widths_i = [np.pi / 8] * len(theta_i)
    colours_i = get_color_gradient(bin_colours[i % len(bin_colours)][0],
                                   bin_colours[i % len(bin_colours)][1],
                                   len(yf[i])
                                   )
    alphas_i = np.linspace(0.1, 0.1, len(radii_i))

    x = center_x - fig_radius * np.cos(angles[i])
    y = center_y - fig_radius * -np.sin(angles[i])
    ax = fig.add_axes([x - 0.09, y - 0.09, 0.18, 0.18], projection='polar')  # Adjust the position and size as needed

    plot_patches(theta_i, radii_i, widths_i, colours_i, ax, radii_offset=0, alphas=alphas_i)

    plt.axis('off')
# plt.tight_layout()  # fill space

if SAVE:
    plt.savefig('../images/polar_per_min_circle_red2blue.png', transparent=True)
    print("saved")
plt.show()

# with and without norm
# with and without radii_offset in plot_patches

import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.io.wavfile import read

from utils.plot_utils import plot_patches, get_color_gradient
from utils.preprocess_audio import sparsify_audio, truncate_and_convert_to_bins, normalize_complex_coords, complex2polar

AUDIO_FILEPATH = sys.argv[1]
SAVE = False
USE_FULL_AUDIO = True

fig = plt.figure(figsize=(10, 10))

#######################################################################################################################
NUM_BINS = 16  # todo or 16
N_PER_BIN = 500  # todo or 35 # SAMPLE_RATE * DURATION
bin_colours = [["#ff0000", "#f9a301"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]]

# read audio
_, original_audio = read(AUDIO_FILEPATH)  # sample_freq = no. of samples per second (Hz), len(audio) = no. data points


def preprocess_border_audio(audio, n_bins, n_per_bin):
    audio = truncate_and_convert_to_bins(audio, n_bins)
    audio = sparsify_audio(audio, n_per_bin)

    # fourier transformation
    yf = fft(audio, axis=-1)

    # Normalize the complex numbers
    yf_norm = normalize_complex_coords(yf)
    # rescale for max is 1
    yf = 1 / np.max(yf_norm, axis=-1, keepdims=True) * yf_norm
    return yf


def plot_boarder(data, n_bins, bin_colours, subplot_radius=0.55):
    # plot organisation
    center_x, center_y = 0.5, 0.5
    fig_radius = subplot_radius # todo or 0.4
    angles = np.linspace(0, np.pi * 2, NUM_BINS, endpoint=False)  # circle

    for i in range(n_bins):
        # plot location = how far in audio
        # radii = as normal
        # theta = full circle (anticlockwise) represents how far in audio for segment

        # complex to polar
        radii_i, _ = complex2polar(data[i])
        theta_i = np.linspace(0, 2 * np.pi, len(radii_i))
        widths_i = [np.pi / 8] * len(theta_i)
        colours_i = get_color_gradient(bin_colours[i % len(bin_colours)][0],
                                       bin_colours[i % len(bin_colours)][1],
                                       len(data[i])
                                       )
        alphas_i = np.linspace(0.1, 0.2, len(radii_i))

        x = center_x - subplot_radius * np.cos(angles[i])
        y = center_y - subplot_radius * -np.sin(angles[i])
        ax = fig.add_axes([x - 0.15, y - 0.15, 0.3, 0.3], projection='polar')  # Adjust the position and size as needed

        plot_patches(theta_i, radii_i, widths_i, colours_i, ax, radii_offset=0, alphas=alphas_i)

        plt.axis('off')

#######################################################################################################################
C_NUM_BINS = 10  # todo or 16
C_N_PER_BIN = 50  # todo or 35
C_bin_colours = [["#ee2ad6", "#f8f242"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]]

# read audio
_, audio = read(AUDIO_FILEPATH)  # sample_freq = no. of samples per second (Hz), len(audio) = no. data points
audio = truncate_and_convert_to_bins(audio, C_NUM_BINS)
audio = sparsify_audio(audio, C_N_PER_BIN)

# fourier transformation
yf = fft(audio, axis=-1)

# Normalize the complex numbers
yf = normalize_complex_coords(yf)

# ax = fig.add_axes([0.5, 0.5, 0.5, 0.5], projection='polar')  # Adjust the position and size as needed
ax = fig.add_subplot(111, projection='polar')

for i in range(C_NUM_BINS):
    # complex to polar
    radii_i, theta_i = complex2polar(yf[i])
    widths_i = np.linspace(np.pi / 32, np.pi / 8, len(theta_i))
    colours_i = get_color_gradient(C_bin_colours[i % len(C_bin_colours)][0],
                                   C_bin_colours[i % len(C_bin_colours)][1],
                                   len(yf[i])
                                   )
    plot_patches(theta_i, radii_i, widths_i, colours_i, ax,
                 radii_offset=i / C_NUM_BINS,
                 alphas=[1 - i / C_NUM_BINS] * len(theta_i))
plt.axis('off')

#######################################################################################################################

if SAVE:
    plt.savefig('../images/polar_per_min_circle_mum_1.png', transparent=False)
    print("saved")
plt.show()

# with and without norm
# with and without radii_offset in plot_patches

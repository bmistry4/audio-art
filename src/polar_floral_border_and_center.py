import sys
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.io.wavfile import read

from utils.plot_utils import plot_patches, get_color_gradient
from utils.preprocess_audio import normalize_complex_coords, complex2polar, apply_preprocessing


########################################################################################################################
class RunID(Enum):
    FINAL = "final"


id_to_plot_shape = {
    RunID.FINAL: (1, 1),
}
########################################################################################################################
ID = RunID.FINAL
save_name = ID.value

SEED = 1111

AUDIO_FILEPATH = sys.argv[1]
SAVE = True
USE_FULL_AUDIO = True

fig = plt.figure(figsize=(10, 10))

#######################################################################################################################
B_NUM_BINS = 16
B_MAX_SAMPLES_PER_BIN = 375
B_BIN_COLOURS = [["#ff0000", "#f9a301"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]]
B_RADII_OFFSET = 0
B_SPASRSIFY_METHOD = "random"

C_NUM_BINS = 10  # todo or 16
C_MAX_SAMPLES_PER_BIN = 31  # todo or 35
C_BIN_COLOURS = [["#ee2ad6", "#f8f242"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]]
C_SPASRSIFY_METHOD = "random"

#######################################################################################################################


def preprocess_border_audio(audio, n_bins, n_per_bin):
    # fixme: sketchy - want each subplot to use the same data so need to reset seed counter
    np.random.seed(SEED)
    processed_audio = apply_preprocessing(audio, B_MAX_SAMPLES_PER_BIN, B_NUM_BINS, sparsify_method=B_SPASRSIFY_METHOD)
    yf = fft(processed_audio, axis=-1)
    # rescale for max is 1
    yf = 1 / np.max(yf, axis=-1, keepdims=True) * yf
    return yf


def plot_boarder(data, n_bins, bin_colours, subplot_radius=0.55):
    # plot organisation
    center_x, center_y = 0.5, 0.5
    angles = np.linspace(0, np.pi * 2, n_bins, endpoint=False)  # circle

    for i in range(n_bins):
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
        # ax = fig.add_axes([x - 0.25, y - 0.25, 0.5, 0.5], projection='polar')  # fixme: for qrcode (thick)
        # ax = fig.add_axes([x - 0.2, y - 0.2, 0.4, 0.4], projection='polar')
        ax = fig.add_axes([x - 0.15, y - 0.15, 0.3, 0.3], projection='polar')  # Adjust the position and size as needed
        # ax = fig.add_axes([x - 0.13, y - 0.13, 0.26, 0.26], projection="polar")  # Adjust the position and size as needed
        # ax = fig.add_axes([x - 0.09, y - 0.09, 0.18, 0.18], projection="polar")  # Adjust the position and size as needed

        plot_patches(theta_i, radii_i, widths_i, colours_i, ax,
                     radius_sf=2,
                     radii_offset=B_RADII_OFFSET,
                     alphas=alphas_i,
                     edge_only=False)

        plt.axis('off')


#######################################################################################################################

def plot_center_piece(original_audio):
    audio = apply_preprocessing(original_audio, C_MAX_SAMPLES_PER_BIN, C_NUM_BINS, sparsify_method=C_SPASRSIFY_METHOD)
    yf = fft(audio, axis=-1)
    yf = normalize_complex_coords(yf)

    ax = fig.add_subplot(111, projection='polar')

    for i in range(C_NUM_BINS):
        # complex to polar
        radii_i, theta_i = complex2polar(yf[i])
        widths_i = np.linspace(np.pi / 32, np.pi / 8, len(theta_i))
        colours_i = get_color_gradient(C_BIN_COLOURS[i % len(C_BIN_COLOURS)][0],
                                       C_BIN_COLOURS[i % len(C_BIN_COLOURS)][1],
                                       len(yf[i])
                                       )
        plot_patches(theta_i, radii_i, widths_i, colours_i, ax,
                     radii_offset=i / C_NUM_BINS,
                     alphas=[1 - i / C_NUM_BINS] * len(theta_i))
    plt.axis('off')


#######################################################################################################################

if __name__ == '__main__':
    _, original_audio = read(AUDIO_FILEPATH)
    yf = preprocess_border_audio(original_audio, B_NUM_BINS, B_MAX_SAMPLES_PER_BIN)
    plot_boarder(yf, B_NUM_BINS, B_BIN_COLOURS, subplot_radius=0.55)
    # plot_center_piece(original_audio)

    if SAVE:
        # plt.savefig('../images/qrcode/FINAL/final-polar-borderAndCenter_dpi-600.png', dpi=600, transparent=False)
        # plt.savefig('../images/qrcode/FINAL/final-polar-center_dpi-600.png', dpi=600, transparent=False)
        plt.savefig('../images/qrcode/FINAL/final-polar-thickBorder_dpi-600.png', dpi=600, transparent=False)
        # plt.savefig('../images/qrcode/FINAL/final-polar-border_dpi-600.png', dpi=600, transparent=False)
        print("saved")
    plt.show()

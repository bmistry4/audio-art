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
    BORDER_AND_CENTER = "final-polar-floral-borderAndCenter_dpi-600"
    CENTER = "final-polar-floral-center_dpi-600"
    BORDER = "final-polar-floral-border_dpi-600"
    THICK_BORDER = "final-polar-floral-thickBorder_dpi-600"
    THICK_BORDER_AND_CENTER = "final-polar-floral-thickBorderAndCenter_dpi-600"


id_to_plot_shape = {
    RunID.BORDER_AND_CENTER: (1, 1),
    RunID.CENTER: (1, 1),
    RunID.BORDER: (1, 1),
    RunID.THICK_BORDER: (1, 1),
    RunID.THICK_BORDER_AND_CENTER: (1, 1),
}
########################################################################################################################
ID = RunID.THICK_BORDER_AND_CENTER
save_name = ID.value

SEED = 1111
np.random.seed(SEED)

AUDIO_FILEPATH = sys.argv[1]
SAVE = True
USE_FULL_AUDIO = True

fig = plt.figure(figsize=(10, 10))
dpi = 600
#######################################################################################################################
B_NUM_BINS = 16
B_MAX_SAMPLES_PER_BIN = 375
B_BIN_COLOURS = [["#ff0000", "#f9a301"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]]
B_RADII_OFFSET = 0
B_SPASRSIFY_METHOD = "random"
B_THICK = True if ID in [RunID.THICK_BORDER, RunID.THICK_BORDER_AND_CENTER] else False

C_NUM_BINS = 10
C_MAX_SAMPLES_PER_BIN = 31
C_BIN_COLOURS = [["#ee2ad6", "#f8f242"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]]
C_SPASRSIFY_METHOD = "random"

#######################################################################################################################


def preprocess_border_audio(data, n_bins, n_per_bin):
    np.random.seed(SEED)
    processed_data = apply_preprocessing(data, n_per_bin, n_bins, sparsify_method=B_SPASRSIFY_METHOD)
    ftt_data = fft(processed_data, axis=-1)
    # rescale for max is 1
    ftt_data = 1 / np.max(ftt_data, axis=-1, keepdims=True) * ftt_data
    return ftt_data


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
        if B_THICK:
            ax = fig.add_axes([x - 0.25, y - 0.25, 0.5, 0.5], projection='polar')
        else:
            ax = fig.add_axes([x - 0.15, y - 0.15, 0.3, 0.3], projection='polar')

        plot_patches(theta_i, radii_i, widths_i, colours_i, ax,
                     radius_sf=2,
                     radii_offset=B_RADII_OFFSET,
                     alphas=alphas_i,
                     edge_only=False)

        plt.axis('off')


#######################################################################################################################

def plot_center_piece(data):
    np.random.seed(SEED)    # comment out to reproduce canvas print
    processed_data = apply_preprocessing(data, C_MAX_SAMPLES_PER_BIN, C_NUM_BINS, sparsify_method=C_SPASRSIFY_METHOD)
    fft_y = fft(processed_data, axis=-1)
    fft_y = normalize_complex_coords(fft_y)

    ax = fig.add_subplot(111, projection='polar')

    for i in range(C_NUM_BINS):
        # complex to polar
        radii_i, theta_i = complex2polar(fft_y[i])
        widths_i = np.linspace(np.pi / 32, np.pi / 8, len(theta_i))
        colours_i = get_color_gradient(C_BIN_COLOURS[i % len(C_BIN_COLOURS)][0],
                                       C_BIN_COLOURS[i % len(C_BIN_COLOURS)][1],
                                       len(fft_y[i])
                                       )
        plot_patches(theta_i, radii_i, widths_i, colours_i, ax,
                     radii_offset=i / C_NUM_BINS,
                     alphas=[1 - i / C_NUM_BINS] * len(theta_i))
    plt.axis('off')


#######################################################################################################################

if __name__ == '__main__':
    _, original_audio = read(AUDIO_FILEPATH)

    if "border" in ID.value.lower():
        fft_audio = preprocess_border_audio(original_audio, B_NUM_BINS, B_MAX_SAMPLES_PER_BIN)
        plot_boarder(fft_audio, B_NUM_BINS, B_BIN_COLOURS, subplot_radius=0.55)
    if "center" in ID.value.lower():
        plot_center_piece(original_audio)

    if SAVE:
        plt.savefig(f'../images/polar-floral-border-and-center/{save_name}.png', dpi=dpi)
        print("saved: ", save_name)
    plt.show()

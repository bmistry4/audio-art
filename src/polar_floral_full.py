import sys
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.io.wavfile import read

from utils.plot_utils import get_color_gradient, plot_patches, switch_off_axes
from utils.preprocess_audio import sparsify_audio, truncate_and_convert_to_bins, complex2polar, \
    normalize_complex_coords, apply_preprocessing

########################################################################################################################
class RunID(Enum):
    FINAL = "final-polar-floral-center_dpi-600" #"final-polar-floral-center-round_dpi-600"
    BASELINE = "0-baseline"
    RADII_OFFSET = "1-radii-offset"
    SPARSIFIES = "2-sparsify"
    USE_NORMALISATION = "3-norm"
    N_BINS = "4-binsNum"
    BIN_SIZE = "5-binsSize"
    COLOURS = "6-colours"


id_to_plot_shape = {
    RunID.FINAL: (1, 1),
    RunID.BASELINE: (2, 4),
    RunID.USE_NORMALISATION: (1, 2),
    RunID.RADII_OFFSET: (2, 3),
    RunID.SPARSIFIES: (1, 3),
    RunID.N_BINS: (2, 3),
    RunID.BIN_SIZE: (2, 3),
    RunID.COLOURS: (2, 2)
}
########################################################################################################################
ID = RunID.FINAL
save_name = ID.value

SEED = 1111
np.random.seed(SEED)

AUDIO_FILEPATH = sys.argv[1]
SAVE = False
USE_FULL_AUDIO = True
IS_TRANSPARENT = False  # True if ID == RunID.FINAL else False

USE_NORMALISATION = [True, False] if ID == RunID.USE_NORMALISATION else [True]
RADII_OFFSET = [0, 0.1, 0.5, 0.8, 1, -1] if ID == RunID.RADII_OFFSET else [-1]

NUM_BINS = [1, 2, 5, 10, 15, 20] if ID == RunID.N_BINS else [10]
MAX_SAMPLES_PER_BIN = [10, 15, 25, 50, 75, 100] if ID == RunID.BIN_SIZE else [50]
SPASRSIFY_METHODS = ["random", "drop", "window-and-random"] if ID == RunID.SPARSIFIES else ["random"]

BIN_COLOURS = [
        [["#ee2ad6", "#f8f242"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]],

        [["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"]],

        [["#967041", "#dfe191"]],

        [["#de4747", "#df3c4e"], ["#df2f55", "#df205e"], ["#dd0b67", "#da0070"], ["#d5007a", "#cf0085"],
         ["#c7008f", "#bd009a"], ["#b100a5", "#a301b0"], ["#9118bb", "#7b26c5"], ["#5e30ce", "#0012ff"]]
    ] if ID == RunID.COLOURS else [
        [["#ee2ad6", "#f8f242"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]]
]

dpi = 600 if ID == RunID.FINAL else None
########################################################################################################################

# read audio
_, audio = read(AUDIO_FILEPATH)

# setup figure and axes
fig, axs = plt.subplots(*id_to_plot_shape[ID], subplot_kw=dict(projection="polar"))
axs_list = axs.ravel() if isinstance(axs, np.ndarray) else [axs]

for bin_idx in range(len(NUM_BINS)):

    for bin_size_idx in range(len(MAX_SAMPLES_PER_BIN)):

        for s_idx in range(len(SPASRSIFY_METHODS)):

            for n_idx in range(len(USE_NORMALISATION)):

                for ro_idx in range(len(RADII_OFFSET)):

                    for c_idx in range(len(BIN_COLOURS)):

                        # set axis index and titles
                        if ID == RunID.FINAL:
                            axs_idx = 0

                        elif ID == RunID.BASELINE:
                            axs_idx = 0
                            fig.set_figheight(3.5)

                        elif ID == RunID.USE_NORMALISATION:
                            axs_idx = n_idx
                            axs_list[axs_idx].set_title(f'{USE_NORMALISATION[n_idx]}')
                            fig.suptitle("Normalise Audio?")

                        elif ID == RunID.RADII_OFFSET:
                            axs_idx = ro_idx
                            if RADII_OFFSET[ro_idx] == -1:
                                sub_title = f"adaptive (0-{i / NUM_BINS[bin_idx]:.2f})"
                            else:
                                sub_title = RADII_OFFSET[ro_idx]
                            axs_list[axs_idx].set_title(f'{sub_title}')
                            fig.suptitle("Radii Offset")

                        elif ID == RunID.SPARSIFIES:
                            axs_idx = s_idx
                            axs_list[axs_idx].set_title(f'{SPASRSIFY_METHODS[s_idx]}')
                            fig.suptitle("Sparsify Methods")
                            fig.set_figheight(3.5)

                        elif ID == RunID.N_BINS:
                            axs_idx = bin_idx
                            axs_list[axs_idx].set_title(f'{NUM_BINS[bin_idx]}')
                            fig.suptitle("Number of Bins")

                        elif ID == RunID.BIN_SIZE:
                            axs_idx = bin_size_idx
                            axs_list[axs_idx].set_title(f'{MAX_SAMPLES_PER_BIN[bin_size_idx]}')
                            fig.suptitle("Samples per Bin")

                        elif ID == RunID.COLOURS:
                            axs_idx = c_idx
                            fig.suptitle("Colours")

                        processed_audio = apply_preprocessing(audio, MAX_SAMPLES_PER_BIN[bin_size_idx],
                                                              NUM_BINS[bin_idx], sparsify_method=SPASRSIFY_METHODS[s_idx])

                        # fourier transformation
                        yf = fft(processed_audio, axis=-1)
                        yf = normalize_complex_coords(yf) if USE_NORMALISATION[n_idx] else yf

                        for i in range(NUM_BINS[bin_idx]):
                            # complex cartesian to polar
                            radii_i, theta_i = complex2polar(yf[i])

                            widths_i = np.linspace(np.pi / 32, np.pi / 8, len(theta_i))

                            bin_colours = BIN_COLOURS[c_idx]
                            colours_i = get_color_gradient(bin_colours[i % len(bin_colours)][0],
                                                           bin_colours[i % len(bin_colours)][1],
                                                           len(yf[i]))
                            radii_offset = i / NUM_BINS[bin_idx] if RADII_OFFSET[ro_idx] == -1 else RADII_OFFSET[ro_idx]

                            if ID == RunID.BASELINE:
                                # add subplot titles
                                for j in range(1, 8):
                                    axs_list[j - 1].set_title(f'{j}')

                                widths_i = [0.8] * len(theta_i)
                                colours_i = ["#1f77b4"] * len(yf[i])    # classic matplotlib blue
                                r_sf = 4.5
                                # show petal with a few data samples. There are  multiple petals because multiple bins.
                                plot_patches([theta_i[0]], [radii_i[0]], widths_i, colours_i, axs_list[0],
                                             radii_offset=0, alphas=[1] * len(theta_i), radius_sf=r_sf)
                                #######################################################################################
                                # all petals
                                plot_patches(theta_i, radii_i, widths_i, colours_i, axs_list[1],
                                             radii_offset=0, alphas=[1] * len(theta_i), radius_sf=r_sf)
                                #######################################################################################
                                # cols
                                colours_i = get_color_gradient(bin_colours[i % len(bin_colours)][0],
                                                               bin_colours[i % len(bin_colours)][1], len(yf[i]))

                                plot_patches(theta_i, radii_i, widths_i, colours_i, axs_list[2],
                                             radii_offset=0, alphas=[1] * len(theta_i), radius_sf=r_sf)
                                #######################################################################################
                                # alphas - fixed
                                plot_patches(theta_i, radii_i, widths_i, colours_i, axs_list[3],
                                             radii_offset=0, alphas=[0.4] * len(theta_i), radius_sf=r_sf)
                                #######################################################################################
                                # alphas - adaptive
                                plot_patches(theta_i, radii_i, widths_i, colours_i, axs_list[4],
                                             radii_offset=0, alphas=[1 - i / NUM_BINS[bin_idx]] * len(theta_i),
                                             radius_sf=r_sf)
                                #######################################################################################
                                # widths
                                widths_i = np.linspace(np.pi / 32, np.pi / 8, len(theta_i))

                                plot_patches(theta_i, radii_i, widths_i, colours_i, axs_list[5],
                                             radii_offset=0, alphas=[1 - i / NUM_BINS[bin_idx]] * len(theta_i),
                                             radius_sf=r_sf)
                                #######################################################################################
                                # edge and facecolour param swap (see plot_patches)
                                plot_patches(theta_i, radii_i, widths_i, colours_i, axs_list[6],
                                             radii_offset=0, alphas=[1 - i / NUM_BINS[bin_idx]] * len(theta_i),
                                             edge_only=True, radius_sf=r_sf)
                                #######################################################################################
                            else:
                                plot_patches(theta_i, radii_i, widths_i, colours_i, axs_list[axs_idx],
                                             radii_offset=radii_offset,
                                             alphas=[1 - i / NUM_BINS[bin_idx]] * len(theta_i)
                                             )

# turn off axis markers
switch_off_axes(axs)

fig.tight_layout()

if SAVE:
    plt.savefig(f'../images/polar-floral-full/{save_name}.png', transparent=IS_TRANSPARENT, dpi=dpi)
    print("saved")

plt.show()

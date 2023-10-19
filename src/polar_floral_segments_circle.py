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
    FINAL = "final-polar-floral-segments-circle"
    BASELINE = "0-baseline"
    SPARSIFIES = "1-sparsify"
    RADII_OFFSET = "2-radii-offset"
    N_BINS = "3-binsNum"
    BIN_SIZE = "4-binsSize"
    COLOURS = "5-colours"


id_to_plot_shape = {
    RunID.FINAL: (1, 1),
    RunID.BASELINE: (1, 1),
    RunID.SPARSIFIES: (1, 1),
    RunID.N_BINS: (1, 1),
    RunID.BIN_SIZE: (1, 1),
    RunID.COLOURS: (1, 1),
    RunID.RADII_OFFSET: (1, 1),
}
########################################################################################################################
ID = RunID.BIN_SIZE
save_name = ID.value

SEED = 1111

AUDIO_FILEPATH = sys.argv[1]
SAVE = True
USE_FULL_AUDIO = True
IS_TRANSPARENT = True if ID == RunID.FINAL else False

RADII_OFFSET = [0, 1] if ID == RunID.RADII_OFFSET else [0]
NUM_BINS = [1, 2, 5, 10, 15, 20] if ID == RunID.N_BINS else [16]
MAX_SAMPLES_PER_BIN = [50, 100, 200, 300, 400, 500] if ID == RunID.BIN_SIZE else [375]
SPASRSIFY_METHODS = ["random", "drop", "window-and-random"] if ID == RunID.SPARSIFIES else ["random"]

BIN_COLOURS = [
    [["#ff0000", "#f9a301"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]],

    [["#de4747", "#df3c4e"], ["#df2f55", "#df205e"], ["#dd0b67", "#da0070"], ["#d5007a", "#cf0085"],
     ["#c7008f", "#bd009a"], ["#b100a5", "#a301b0"], ["#9118bb", "#7b26c5"], ["#5e30ce", "#0012ff"]],

    [["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"]],

    [["#ff0000", "#ff000f", ],
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
] if ID == RunID.COLOURS else [
        [["#ff0000", "#f9a301"], ["#61f31d", "#16d5c1"], ["#7270e8", "#e87070"], ["#f75919", "#f2fa00"]],
]

# read audio
_, audio = read(AUDIO_FILEPATH)  # sample_freq = no. of samples per second (Hz), len(audio) = no. data points
# audio = truncate_and_convert_to_bins(audio, NUM_BINS)
# processed_audio = sparsify_audio(audio, N_PER_BIN)

for bin_size_idx in range(len(MAX_SAMPLES_PER_BIN)):

    for s_idx in range(len(SPASRSIFY_METHODS)):

        for ro_idx in range(len(RADII_OFFSET)):

            for c_idx in range(len(BIN_COLOURS)):

                for bin_idx in range(len(NUM_BINS)):
                    # setup figure and axes
                    fig, axs = plt.subplots(NUM_BINS[bin_idx], subplot_kw=dict(projection="polar"))
                    fig.set_figheight(10)
                    fig.set_figwidth(10)
                    axs_list = axs.ravel() if isinstance(axs, np.ndarray) else [axs]
                    save_name = ID.value

                    # set axis index and titles
                    if ID == RunID.FINAL:
                        axs_idx = 0

                    elif ID == RunID.BASELINE:
                        axs_idx = 0

                    elif ID == RunID.RADII_OFFSET:
                        axs_idx = ro_idx
                        save_name += f"-{RADII_OFFSET[ro_idx]}"

                    elif ID == RunID.SPARSIFIES:
                        axs_idx = s_idx
                        save_name += f"-{SPASRSIFY_METHODS[s_idx]}"

                    elif ID == RunID.N_BINS:
                        axs_idx = bin_idx
                        save_name += f"-{NUM_BINS[bin_idx]}"

                    elif ID == RunID.BIN_SIZE:
                        axs_idx = bin_size_idx
                        save_name += f"-{MAX_SAMPLES_PER_BIN[bin_size_idx]}"

                    elif ID == RunID.COLOURS:
                        axs_idx = c_idx
                        save_name += f"-{c_idx}"

                    # fixme: sketchy - want each subplot to use the same data so need to reset seed counter
                    np.random.seed(SEED)
                    processed_audio = apply_preprocessing(audio, MAX_SAMPLES_PER_BIN[bin_size_idx], NUM_BINS[bin_idx],
                                                          sparsify_method=SPASRSIFY_METHODS[s_idx])

                    # fourier transformation
                    yf = fft(processed_audio, axis=-1)

                    # rescale for max is 1
                    yf = 1 / np.max(yf, axis=-1, keepdims=True) * yf

                    # plot organisation
                    center_x, center_y = 0.5, 0.5
                    fig_radius = 0.4
                    angles = np.linspace(0, np.pi * 2, NUM_BINS[bin_idx], endpoint=False)  # circle

                    for b_idx in range(NUM_BINS[bin_idx]):
                        # todo - remove notes once readme is updated
                        # plot location = how far in audio
                        # radii = as normal
                        # theta = full circle (anticlockwise) represents how far in audio for segment

                        # complex to polar
                        radii_i, _ = complex2polar(yf[b_idx])

                        theta_i = np.linspace(0, 2 * np.pi, len(radii_i))
                        widths_i = [np.pi / 8] * len(theta_i)
                        bin_colours = BIN_COLOURS[c_idx]
                        colours_i = get_color_gradient(bin_colours[b_idx % len(bin_colours)][0],
                                                       bin_colours[b_idx % len(bin_colours)][1], len(yf[b_idx]))
                        alphas_i = np.linspace(0.1, 0.1, len(radii_i))

                        x = center_x - fig_radius * np.cos(angles[b_idx])
                        y = center_y - fig_radius * -np.sin(angles[b_idx])
                        axs_list[b_idx].set_position([x - 0.09, y - 0.09, 0.18, 0.18])
                        # ax = fig.add_axes([x - 0.09, y - 0.09, 0.18, 0.18], projection='polar')  # Adjust the position and size as needed

                        # todo - edge only alternate with alpha set to higher
                        plot_patches(theta_i, radii_i, widths_i, colours_i, axs_list[b_idx], radius_sf=2,
                                     radii_offset=RADII_OFFSET[ro_idx], alphas=alphas_i, edge_only=False)

                    # turn off axis markers
                    switch_off_axes(axs)

                    if SAVE:

                        plt.savefig(f'../images/polar-floral-segments-circle/{save_name}.png',
                                    transparent=IS_TRANSPARENT)
                        print("saved")

                    plt.show()

# with and without norm
# with and without radii_offset (=1) in plot_patches with alpha ~0.3

"""
https://python-graph-gallery.com/streamchart-basic-matplotlib/
"""

import sys
from enum import Enum

import matplotlib.pyplot as plt
from scipy import stats
from scipy.io.wavfile import read

from utils.plot_utils import *
from utils.preprocess_audio import *

########################################################################################################################
class RunID(Enum):
    FINAL = "final-frequency-waves-overlapping"
    GAUSSIAN = "0-gaussian"
    COLOUR_AND_ALPHA = "1-gaussian-cols-alphas"
    G_BASLINES = "2-gaussianBaselines-cols-alphas"
    SPARSIFIES = "3-gaussianBaselines-cols-alphas-sparsify"
    G_SDEVS = "4-gaussianSym-sdev"
    G_OFFSETS = "5-gaussianSym-gaussianOffset"
    N_BINS = "6-gaussianSym-binsNum"
    BIN_SIZE = "7-gaussianSym-binsSize"
    COLOURS = "8-gaussianSym-colours"


id_to_plot_shape = {
    RunID.FINAL: (1, 1),
    RunID.GAUSSIAN: (3, 1),
    RunID.COLOUR_AND_ALPHA: (3, 1),
    RunID.G_BASLINES: (3, 1),
    RunID.SPARSIFIES: (3, 1),
    RunID.G_SDEVS: (2, 2),
    RunID.G_OFFSETS: (3, 2),
    RunID.N_BINS: (3, 2),
    RunID.BIN_SIZE: (3, 2),
    RunID.COLOURS: (3, 2),
}

########################################################################################################################
ID = RunID.FINAL
save_name = ID.value

SEED = 1111
np.random.seed(SEED)

AUDIO_FILEPATH = sys.argv[1]
SAVE = False
USE_FULL_AUDIO = True
IS_TRANSPARENT = False

NUM_BINS = [30]                 # [2, 15, 30, 45, 60, 75]
MAX_SAMPLES_PER_BIN = [500]     # [10, 100, 250, 500, 750, 1000]

SDEVS = [15]                    # [1, 5, 15, 50]
GAUSSIAN_OFFSETS = [50]         # [-50, -25, 0, 25, 50]

SPASRSIFY_METHODS = ["window-and-random"]  # ["random", "drop", "window-and-random"]

COLOURS = [("#ed5394", "#eda253")]  # [("#0012ff", "#ff0000"), ("#0F45D2", "#bce1d0"), ("#ed5394", "#eda253"), ("#6453ed", "#66ed53"), ("#967041", "#dfe191"), ("#ffffff", "#000000")]
alpha_range = [0.8, 0.4]


########################################################################################################################

def gaussian_smooth(x, y, sd=1):
    weights = np.array([stats.norm.pdf(x, m, sd) for m in x])
    weights = weights / weights.sum(1)
    return (weights * y).sum(1)


def gaussian_smooth_grid(x, y, grid, sd):
    # todo - multiprocessing/pooling?
    weights = np.transpose([stats.norm.pdf(grid, m, sd) for m in x])
    weights = weights / weights.sum(0)
    return (weights * y).sum(1)


########################################################################################################################
if __name__ == '__main__':
    # read audio
    sample_freq, audio = read(AUDIO_FILEPATH)

    # for dev: only use partial audio (select from range of mins)
    if not USE_FULL_AUDIO:
        audio = snip_audio(audio, [0, 3], sample_freq)

    # setup figure and axes
    fig, axs = plt.subplots(*id_to_plot_shape[ID])
    axs_list = axs.ravel() if isinstance(axs, np.ndarray) else [axs]

    for col_idx in range(len(COLOURS)):
        colour_1, colour_2 = COLOURS[col_idx]

        for bin_idx in range(len(NUM_BINS)):
            # get colours and alphas
            colours = get_color_gradient(colour_1, colour_2, NUM_BINS[bin_idx])
            alphas = get_alphas(alpha_range[0], alpha_range[1], NUM_BINS[bin_idx])

            for bin_size_idx in range(len(MAX_SAMPLES_PER_BIN)):

                for sd_idx in range(len(SDEVS)):

                    for go_idx in range(len(GAUSSIAN_OFFSETS)):

                        for s_idx in range(len(SPASRSIFY_METHODS)):
                            # fixme: sketchy - want each subplot to use the same data so need to reset seed counter
                            np.random.seed(SEED)

                            # preprocessing audio
                            processed_audio = apply_preprocessing(audio, MAX_SAMPLES_PER_BIN[bin_size_idx],
                                                                  NUM_BINS[bin_idx], sparsify_method=SPASRSIFY_METHODS[s_idx])
                            dp_per_bin = processed_audio.shape[1]

                            x = np.arange(0, dp_per_bin)
                            y = processed_audio

                            # gaussian smooth
                            y_smoothed = [gaussian_smooth(x, y_, 1) for y_ in y]

                            # grid smooth gaussian
                            grid = np.linspace(-GAUSSIAN_OFFSETS[go_idx], dp_per_bin + GAUSSIAN_OFFSETS[go_idx], num=len(x))
                            y_smoothed_grid = [gaussian_smooth_grid(x, y_, grid, SDEVS[sd_idx]) for y_ in y]

                            ###########################################################################################
                            if ID == RunID.FINAL:
                                fig.set_figwidth(10)
                                fig.set_figheight(7)
                                axs.stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)

                            elif ID == RunID.GAUSSIAN:
                                axs[0].stackplot(x, y)
                                axs[1].stackplot(x, y_smoothed, baseline='zero')
                                axs[2].stackplot(x, y_smoothed_grid, baseline='zero')
                                axs[0].set_title('stackplot')
                                axs[1].set_title('+ gaussian smoothing')
                                axs[2].set_title('+ gaussian grid smoothing')

                            elif ID == RunID.COLOUR_AND_ALPHA:
                                axs[0].stackplot(x, y_smoothed_grid, baseline='zero')
                                axs[1].stackplot(x, y_smoothed_grid, baseline='zero', colors=colours)
                                axs[2].stackplot(x, y_smoothed_grid, baseline='zero', colors=colours, alpha=alphas)
                                axs[0].set_title('base')
                                axs[1].set_title('+ colour')
                                axs[2].set_title('+ colour + alpha')

                            elif ID == RunID.G_BASLINES:
                                axs[0].stackplot(x, y_smoothed_grid, baseline='zero', colors=colours, alpha=alphas)
                                axs[1].stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)
                                axs[2].stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)
                                axs[0].set_title('baseline="zero"')
                                axs[1].set_title('baseline="wiggle"')
                                axs[2].set_title('baseline="sym"')

                            elif ID == RunID.SPARSIFIES:
                                axs_list[s_idx].stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)
                                axs_list[s_idx].set_title(f'{SPASRSIFY_METHODS[s_idx]}')

                            elif ID == RunID.G_SDEVS:
                                axs_list[sd_idx].stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)
                                axs_list[sd_idx].set_title(f'sd: {SDEVS[sd_idx]}, gaussian offset: {GAUSSIAN_OFFSETS[go_idx]}')

                            elif ID == RunID.G_OFFSETS:
                                axs_list[go_idx].stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)
                                axs_list[go_idx].set_title(f'sd: {SDEVS[sd_idx]}, gaussian offset: {GAUSSIAN_OFFSETS[go_idx]}')

                            elif ID == RunID.N_BINS:
                                axs_list[bin_idx].stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)
                                axs_list[bin_idx].set_title(f'#bins: {NUM_BINS[bin_idx]}, bin size: {MAX_SAMPLES_PER_BIN[bin_size_idx]}')

                            elif ID == RunID.BIN_SIZE:
                                axs_list[bin_size_idx].stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)
                                axs_list[bin_size_idx].set_title(f'#bins: {NUM_BINS[bin_idx]}, bin size: {MAX_SAMPLES_PER_BIN[bin_size_idx]}')

                            elif ID == RunID.COLOURS:
                                axs_list[col_idx].stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)
                                axs_list[col_idx].set_title(f'{COLOURS[col_idx][0]} - {COLOURS[col_idx][1]}')

                            else:
                                raise KeyError(f"Invalid ID (={ID}) given")

    # turn off axis markers
    switch_off_axes(axs)

    # fill space
    plt.tight_layout()

    if SAVE:
        plt.savefig(f'../images/freq-waves-overlapping/{save_name}.png', transparent=IS_TRANSPARENT)
        print("saved")

    plt.show()

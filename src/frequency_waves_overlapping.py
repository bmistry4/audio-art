"""
https://python-graph-gallery.com/streamchart-basic-matplotlib/
"""

import sys
import random

import matplotlib.pyplot as plt
from scipy import stats
from scipy.io.wavfile import read

from utils.plot_utils import *
from utils.preprocess_audio import *

########################################################################################################################
# fixme - random sparsify gives diff outputs for each subplot! seeding isn't working
AUDIO_FILEPATH = sys.argv[1]
SAVE = False
USE_FULL_AUDIO = False
IS_TRANSPARENT = False

NUM_BINS = [15]                 # [2, 15, 30, 45, 60, 75]   #[30]   # todo
MAX_SAMPLES_PER_BIN = [100]     # [10, 100, 250, 500, 750, 1000] #[500] # todo

SDEVS = [15]                    # [1, 5, 15, 50]
GAUSSIAN_OFFSETS = [50]         # [-50, -25, 0, 25, 50]

SPASRSIFY_METHODS = ["random"]  # ["random", "drop", "window-and-random"]

COLOURS = [("#0012ff", "#ff0000"), ("#0F45D2", "#bce1d0"), ("#ed5394", "#eda253"),
           ("#6453ed", "#66ed53"), ("#967041", "#dfe191"), ("#ffffff", "#000000")]
alpha_range = [0.8, 0.4]

save_name = "frequency_waves_overlapping"
########################################################################################################################
def gaussian_smooth(x, y, sd=1):
    weights = np.array([stats.norm.pdf(x, m, sd) for m in x])
    weights = weights / weights.sum(1)
    return (weights * y).sum(1)


#todo - multiprocessing?
def gaussian_smooth_grid(x, y, grid, sd):
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

    # save_name = "3-gaussianBaselines-cols-alphas-sparsify"
    # save_name = "4-gaussianWiggle-sdev-cols-alphas-sparsify"
    # save_name = "5-gaussianWiggle-gaussianOffset-cols-alphas-sparsify"
    # save_name = "6-gaussianWiggle-cols-alphas-sparsify-binsNum"
    # save_name = "7-gaussianWiggle-cols-alphas-sparsify-binsSize"
    save_name = "8-gaussianWiggle-cols-alphas-sparsify-colours"

    fig, axs = plt.subplots(3, 2)
    axs_list = axs.ravel()

    for col_idx in range(len(COLOURS)):
        colour_1, colour_2 = COLOURS[col_idx]

        for bin_idx in range(len(NUM_BINS)):

            colours = get_color_gradient(colour_1, colour_2, NUM_BINS[bin_idx])
            alphas = get_alphas(alpha_range[0], alpha_range[1], NUM_BINS[bin_idx])

            for bin_size_idx in range(len(MAX_SAMPLES_PER_BIN)):

                for sd_idx in range(len(SDEVS)):

                    for go_idx in range(len(GAUSSIAN_OFFSETS)):

                        for s_idx, sparsify_method in enumerate(SPASRSIFY_METHODS):
                            processed_audio = apply_preprocessing(audio, MAX_SAMPLES_PER_BIN[bin_size_idx],
                                                                  NUM_BINS[bin_idx], sparsify_method=sparsify_method)

                            # plot graph
                            dp_per_bin = processed_audio.shape[1]
                            x = np.arange(0, dp_per_bin)
                            y = processed_audio

                            # gaussian smooth
                            y_smoothed = [gaussian_smooth(x, y_, 1) for y_ in y]

                            # grid smooth gaussian
                            grid = np.linspace(-GAUSSIAN_OFFSETS[go_idx], dp_per_bin + GAUSSIAN_OFFSETS[go_idx], num=len(x))
                            y_smoothed_grid = [gaussian_smooth_grid(x, y_, grid, SDEVS[sd_idx]) for y_ in y]

                            # temp
                            # fig, ax = plt.subplots(figsize=(10, 7))
                            # ax.stackplot(x, y)
                            # ax.stackplot(x, y_smoothed, baseline='zero')
                            # ax.stackplot(x, y_smoothed_grid, baseline='zero')
                            # ax.stackplot(x, y_smoothed_grid, baseline='zero', colors=colours)
                            # ax.stackplot(x, y_smoothed_grid, baseline='zero', colors=colours, alpha=alphas)
                            # ax.stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)
                            # ax.stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)
                            # plt.axis('off')

                            # 0-gaussian
                            # save_name = "0-gaussian"
                            # fig, axs = plt.subplots(3, 1)
                            # axs[0].stackplot(x, y)
                            # axs[1].stackplot(x, y_smoothed, baseline='zero')
                            # axs[2].stackplot(x, y_smoothed_grid, baseline='zero')
                            # axs[0].set_title('stackplot')
                            # axs[1].set_title('+ gaussian smoothing')
                            # axs[2].set_title('+ gaussian grid smoothing')

                            # 1-gaussian-cols-alphas.png
                            # save_name = "1-gaussian-cols-alphas"
                            # fig, axs = plt.subplots(3, 1)
                            # axs[0].stackplot(x, y_smoothed_grid, baseline='zero')
                            # axs[1].stackplot(x, y_smoothed_grid, baseline='zero', colors=colours)
                            # axs[2].stackplot(x, y_smoothed_grid, baseline='zero', colors=colours, alpha=alphas)
                            # axs[0].set_title('base')
                            # axs[1].set_title('+ colour')
                            # axs[2].set_title('+ colour + alpha')

                            # 2-gaussianBaselines-cols-alphas
                            # save_name = "2-gaussianBaselines-cols-alphas"
                            # fig, axs = plt.subplots(3, 1)
                            # axs[0].stackplot(x, y_smoothed_grid, baseline='zero', colors=colours, alpha=alphas)
                            # axs[1].stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)
                            # axs[2].stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)
                            # axs[0].set_title('baseline="zero"')
                            # axs[1].set_title('baseline="wiggle"')
                            # axs[2].set_title('baseline="sym"')

                            # 3-gaussianBaselines-cols-alphas-sparsify
                            # axs_list[s_idx].stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)
                            # axs_list[s_idx].set_title(f'{sparsify_method}')

                            # 4-gaussianWiggle-sdev-cols-alphas-sparsify
                            # axs_list[sd_idx].stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)
                            # axs_list[sd_idx].set_title(f'sd: {SDEVS[sd_idx]}, gaussian offset: {GAUSSIAN_OFFSETS[go_idx]}')

                            # "5-gaussianWiggle-gaussianOffset-cols-alphas-sparsify"
                            # axs_list[go_idx].stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)
                            # axs_list[go_idx].set_title(f'sd: {SDEVS[sd_idx]}, gaussian offset: {GAUSSIAN_OFFSETS[go_idx]}')

                            # "6-gaussianWiggle-cols-alphas-sparsify-binsNum"
                            # axs_list[bin_idx].stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)
                            # axs_list[bin_idx].set_title(f'#bins: {NUM_BINS[bin_idx]}, bin size: {MAX_SAMPLES_PER_BIN[bin_size_idx]}')

                            # "7-gaussianWiggle-cols-alphas-sparsify-binsSize"
                            # axs_list[bin_size_idx].stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)
                            # axs_list[bin_size_idx].set_title(
                            #     f'#bins: {NUM_BINS[bin_idx]}, bin size: {MAX_SAMPLES_PER_BIN[bin_size_idx]}')

                            "8-gaussianWiggle-cols-alphas-sparsify-colours"
                            axs_list[col_idx].stackplot(x, y_smoothed_grid, baseline='wiggle', colors=colours, alpha=alphas)
                            axs_list[col_idx].set_title(f'{COLOURS[col_idx][0]} - {COLOURS[col_idx][1]}')

    for ax in axs.ravel():
        ax.set_axis_off()

    plt.tight_layout()  # fill space

    if SAVE:
        plt.savefig(f'../images/freq-waves-overlapping/{save_name}.png', transparent=IS_TRANSPARENT)
        print("saved")

    plt.show()

    # VARIATIONS TO PLOT EVOLUTION
    # no colouring, no gaussian,
    # no colouring, gaussian
    # no colouring, gaussian grid

    # colouring, gaussian grid
    # colouring, gaussian grid, alphas

    # colouring, gaussian grid, alphas, diff baseline params

    # colouring, gaussian grid, alphas, diff sparsify methods

    # colouring, gaussian grid, alphas, diff gaussian hparams

    # different bins and samples per bin

    # diff colours

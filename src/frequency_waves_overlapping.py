"""
https://python-graph-gallery.com/streamchart-basic-matplotlib/
"""

import sys

import matplotlib.pyplot as plt
from scipy import stats
from scipy.io.wavfile import read

from utils.plot_utils import *
from utils.preprocess_audio import *

# 15 mins 38 secs == #.0378333333333 secs
AUDIO_FILEPATH = sys.argv[1]
SAVE = False
USE_FULL_AUDIO = True

NUM_BINS = 30
MAX_SAMPLES_PER_BIN = 500

SDEV = 15  # todo - hparam ; bigger is smoother
GAUSSIAN_OFFSET = 50  # todo - hparam

# color_1 = "#0F45D2"
# color_2 = "#bce1d0"
color_1 = "#0012ff"
color_2 = "#ff0000"
alpha_range = [0.8, 0.4]


########################################################################################################################
# def gaussian_smooth(x, y, sd=1):
#     weights = np.array([stats.norm.pdf(x, m, sd) for m in x])
#     weights = weights / weights.sum(1)
#     return (weights * y).sum(1)


def gaussian_smooth_grid(x, y, grid, sd):
    weights = np.transpose([stats.norm.pdf(grid, m, sd) for m in x])
    weights = weights / weights.sum(0)
    return (weights * y).sum(1)


########################################################################################################################
if __name__ == '__main__':

    colours = get_color_gradient(color_1, color_2, NUM_BINS)
    alphas = get_alphas(alpha_range[0], alpha_range[1], NUM_BINS)

    # read audio
    sample_freq, audio = read(
        AUDIO_FILEPATH)  # sample_freq = no. of samples per second (Hz), len(audio) = no. data points

    # only use partial audio (select from range of mins)
    if not USE_FULL_AUDIO:
        audio = snip_audio(audio, [0, 9], sample_freq)

    audio = convert_to_bins(audio, NUM_BINS)
    # audio = audio / audio.max(1)[:, numpy.newaxis]  # max normalisation

    # positive values only # todo abs
    # audio = np.abs(audio)

    audio = sparsify_audio(audio, MAX_SAMPLES_PER_BIN)

    # plot graph
    dp_per_bin = audio.shape[1]
    x = np.arange(0, dp_per_bin)
    y = audio
    # y_smoothed = [gaussian_smooth(x, y_, 1) for y_ in y]
    grid = np.linspace(-GAUSSIAN_OFFSET, dp_per_bin + GAUSSIAN_OFFSET, num=len(x))
    y_smoothed_grid = [gaussian_smooth_grid(x, y_, grid, SDEV) for y_ in y]

    fig, ax = plt.subplots(figsize=(10, 7))
    # ax.stackplot(x, y, baseline='zero', colors=colours, alpha=alphas)
    # ax.stackplot(x, y_smoothed, baseline='zero')
    ax.stackplot(x, y_smoothed_grid, baseline='sym', colors=colours, alpha=alphas)  # todo - try diff baseline

    plt.axis('off')
    plt.tight_layout()  # fill space

    if SAVE:
        plt.savefig('../images/audio-visual-blue2red.png', transparent=True)
        print("saved")

    plt.show()

    # VARIATIONS TO PLOT EVOLUTION
    # no colouring, no gaussian, small dps
    # no colouring, gaussian with different baseline args
    # no colouring, gaussian with diff hparams
    # colouring, gaussian
    # coluring + alphas, gaussian
    # colouring, abs(audio)
    # without axes tight layout

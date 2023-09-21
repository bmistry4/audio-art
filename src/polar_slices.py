# https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_bar.html
import sys
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.io.wavfile import read

from utils.plot_utils import get_color_gradient
from utils.preprocess_audio import complex2polar, apply_preprocessing


########################################################################################################################
class RunID(Enum):
    FINAL = "final-polar-slices"
    SIMPLE = "0-simple"
    SPARSIFY = "1-sparsify-methods"
    N_SAMPLES = "2-max-samples"
    COLOURS = "3-colours"
    ALPHAS = "4-alphas"
    ALPHAS_LOGY = "5-alphas-logY"


id_to_plot_shape = {
    RunID.FINAL: (1, 1),
    RunID.SIMPLE: (1, 1),
    RunID.SPARSIFY: (1, 3),
    RunID.N_SAMPLES: (2, 3),
    RunID.COLOURS: (2, 3),
    RunID.ALPHAS: (2, 4),
    RunID.ALPHAS_LOGY: (2, 4),
}

########################################################################################################################
ID = RunID.FINAL
save_name = ID.value

SEED = 1111
np.random.seed(SEED)


AUDIO_FILEPATH = sys.argv[1]
SAVE = False
IS_TRANSPARENT = False
USE_LOG_Y = False

# TODO - set params
MAX_SAMPLES = [150] #[50, 150, 250, 350, 450, 550]# [150] # SAMPLE_RATE * DURATION
SPASRSIFY_METHODS =  ["random"] #["random", "drop", "window-and-random"]
COLOURS = [("#8d7ed8", "#5bffef")]  # [("#0012ff", "#ff0000"), ("#0F45D2", "#bce1d0"), ("#ed5394", "#eda253"), ("#6453ed", "#66ed53"), ("#967041", "#dfe191"), ("#ffffff", "#000000")]
ALPHAS = [0.4] #[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

########################################################################################################################
# read audio
sample_freq, audio = read(AUDIO_FILEPATH)  # sample_freq = no. of samples per second (Hz), len(audio) = no. data points

# setup figure and axes
fig, axs = plt.subplots(*id_to_plot_shape[ID], subplot_kw=dict(projection="polar"))
axs_list = axs.ravel() if isinstance(axs, np.ndarray) else [axs]

for n_idx in range(len(MAX_SAMPLES)):

    for s_idx in range(len(SPASRSIFY_METHODS)):
        # fixme: sketchy - want each subplot to use the same data so need to reset seed counter
        np.random.seed(SEED)
        processed_audio = apply_preprocessing(audio, MAX_SAMPLES[n_idx], 1, sparsify_method=SPASRSIFY_METHODS[s_idx])
        processed_audio = processed_audio.flatten()

        # fourier transformation
        yf = fft(processed_audio)
        # complex to polar
        radii, theta = complex2polar(yf)

        for col_idx in range(len(COLOURS)):
            colour_1, colour_2 = COLOURS[col_idx]
            colours = get_color_gradient(colour_1, colour_2, MAX_SAMPLES[n_idx])

            for alp_idx in range(len(ALPHAS)):

                # time = bar width and colour
                if ID == RunID.SIMPLE or ID == RunID.FINAL:
                    axs_idx = 0

                elif ID == RunID.COLOURS:
                    assert len(COLOURS) > 1, f"{RunID.COLOURS} run needs multiple colours to plot"
                    axs_idx = col_idx
                    axs_list[axs_idx].set_title(f'{COLOURS[col_idx][0]} - {COLOURS[col_idx][1]}')
                    fig.suptitle("Colours")

                elif ID == RunID.N_SAMPLES:
                    assert len(MAX_SAMPLES) > 1, f"{RunID.N_SAMPLES} run needs multiple max samples to plot"
                    axs_idx = n_idx
                    axs_list[axs_idx].set_title(f'{MAX_SAMPLES[n_idx]}')
                    fig.suptitle("Total Number of Data Samples")

                elif ID == RunID.SPARSIFY:
                    assert len(SPASRSIFY_METHODS) > 1, f"{RunID.SPARSIFY} run needs multiple sparsify methods to plot"
                    axs_idx = s_idx
                    axs_list[axs_idx].set_title(f'{SPASRSIFY_METHODS[s_idx]}')
                    fig.suptitle("Sparsify Methods")
                    fig.set_figheight(3.5)

                elif ID == RunID.ALPHAS:
                    assert len(ALPHAS) > 1, f"{RunID.ALPHAS} run needs multiple alphas to plot"
                    axs_idx = alp_idx
                    axs_list[axs_idx].set_title(f'{ALPHAS[alp_idx]}')
                    fig.suptitle("Alphas")

                elif ID == RunID.ALPHAS_LOGY:
                    assert len(ALPHAS) > 1, f"{RunID.ALPHAS_LOGY} run needs multiple alphas to plot"
                    axs_idx = alp_idx
                    USE_LOG_Y = True
                    axs_list[axs_idx].set_title(f'{ALPHAS[alp_idx]}')
                    fig.suptitle("Alphas and log y-axis")

                else:
                    raise KeyError(f"Invalid ID (={ID}) given")

                axs_list[axs_idx].bar(theta, radii, width=np.linspace(np.pi / 32, np.pi / 8, len(theta)), bottom=0.0,
                                      color=colours, alpha=ALPHAS[alp_idx], align='edge', log=USE_LOG_Y)

# turn off axis markers
if isinstance(axs, np.ndarray):
    for ax in axs.ravel():
        ax.set_axis_off()
else:
    axs.set_axis_off()

fig.tight_layout()

if SAVE:
    plt.savefig(f'../images/polar-slices/{save_name}.png', transparent=IS_TRANSPARENT)
    print("saved")

plt.show()
print("completed")

# https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_bar.html
import sys
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.io.wavfile import read

from utils.plot_utils import get_color_gradient, switch_off_axes
from utils.preprocess_audio import complex2polar, apply_preprocessing


########################################################################################################################
class RunID(Enum):
    FINAL = "final-polar-slices_dpi-600"
    BASELINE = "0-baseline"
    SPARSIFIES = "1-sparsify-methods"
    N_SAMPLES = "2-max-samples"
    COLOURS = "3-colours"
    ALPHAS = "4-alphas"
    ALPHAS_LOGY = "5-alphas-logY"


id_to_plot_shape = {
    RunID.FINAL: (1, 1),
    RunID.BASELINE: (2, 2),
    RunID.SPARSIFIES: (1, 3),
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

AUDIO_FILEPATH = sys.argv[1]    # path to audio file
SAVE = False
IS_TRANSPARENT = False
USE_LOG_Y = False

MAX_SAMPLES = [50, 150, 250, 350, 450, 550] if ID == RunID.N_SAMPLES else [150]
SPASRSIFY_METHODS = ["random", "drop", "window-and-random"] if ID == RunID.SPARSIFIES else ["random"]
COLOURS = [
    ("#0012ff", "#ff0000"),
    ("#0F45D2", "#bce1d0"),
    ("#ed5394", "#eda253"),
    ("#6453ed", "#66ed53"),
    ("#967041", "#dfe191"),
    ("#ffffff", "#000000")
] if ID == RunID.COLOURS else [("#8d7ed8", "#5bffef")]
ALPHAS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8] if ID in [RunID.ALPHAS, RunID.ALPHAS_LOGY] else [0.4]

dpi = 600 if ID == RunID.FINAL else None
########################################################################################################################
# read audio
_, audio = read(AUDIO_FILEPATH)

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

                if ID == RunID.BASELINE:
                    axs_list[0].bar(theta, radii, align='edge')
                    axs_list[1].bar(theta, radii, alpha=ALPHAS[alp_idx], align='edge')
                    axs_list[2].bar(theta, radii, alpha=ALPHAS[alp_idx], align='edge',
                                    width=np.linspace(np.pi / 32, np.pi / 8, len(theta)))
                    axs_list[3].bar(theta, radii, alpha=ALPHAS[alp_idx], align='edge',
                                    width=np.linspace(np.pi / 32, np.pi / 8, len(theta)), color=colours)

                    axs_list[0].set_title(f'1) default polar bar plot')
                    axs_list[1].set_title(f'2) + alpha')
                    axs_list[2].set_title(f'3) + incremental bar width')
                    axs_list[3].set_title(f'4) + colours')
                    break

                elif ID == RunID.FINAL:
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

                elif ID == RunID.SPARSIFIES:
                    assert len(SPASRSIFY_METHODS) > 1, f"{RunID.SPARSIFIES} run needs multiple sparsify methods to plot"
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

                # time = bar width and colour
                axs_list[axs_idx].bar(theta, radii, width=np.linspace(np.pi / 32, np.pi / 8, len(theta)), bottom=0.0,
                                      color=colours, alpha=ALPHAS[alp_idx], align='edge', log=USE_LOG_Y)

# turn off axis markers
switch_off_axes(axs)

fig.tight_layout()

if SAVE:
    plt.savefig(f'../images/polar-slices/{save_name}.png', transparent=IS_TRANSPARENT, dpi=dpi)
    print("saved")

plt.show()
print("completed")

import sys
import wave

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read

from utils.plot_utils import get_color_gradient

# 15 mins 38 secs == 983.0378333333333 secs
AUDIO_FILEPATH = sys.argv[1]

########################################################################################################################
# PRINT BASIC AUDIO STATS - https://realpython.com/python-scipy-fft/
with wave.open(AUDIO_FILEPATH, 'rb') as wav_obj:
    sample_freq = wav_obj.getframerate()  # number of samples per second
    n_samples = wav_obj.getnframes()  # number of individual frames, or samples
    t_audio = n_samples / sample_freq  # audio length (secs)
    n_channels = wav_obj.getnchannels()  # no. channels e.g. if recorded in stereo = 2 channels (left and right)

    print(f"sample freq: {sample_freq} Hz,\n"
          f"no. samples: {n_samples} data points,\n"
          f"audio len: {t_audio} secs,\n"
          f"no. channels: {n_channels}"
          )


########################################################################################################################
# signal_wave = wav_obj.readframes(n_samples)                       # wave amplitude array in bytes
# signal_array = np.frombuffer(signal_wave, dtype=np.int16)
# times = np.linspace(0, (2*n_samples)/sample_freq, num=2*n_samples)      # times where each sample is taken
#
# plt.figure(figsize=(15, 5))
# plt.plot(times, signal_array)
# plt.title('Wave')
# plt.ylabel('Signal Value')
# plt.xlabel('Time (s)')
# plt.xlim(0, t_audio)
# plt.show()
#


plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
# plt.style.use("ggplot")
# ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background',
# 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind',
# 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted',
# 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk',
# 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
color1 = "#0F45D2"
color2 = "#bce1d0"

# len(audio) = no. data points/ samples
sample_freq, audio = read(AUDIO_FILEPATH)

# Check the data type of audio_data
data_type = audio.dtype
print(f"Data type of audio_data: {data_type}")

# Check the bit depth (number of bits per sample)
bit_depth = audio.dtype.itemsize * 8  # get number of bytes and mul by 8 to get no. of bits
print(f"Bit depth: {bit_depth} bits")


STEP = 1
AUDIO_MINS = 16  # int(t_audio // 60)
MAX_MINS = AUDIO_MINS - STEP
colours = get_color_gradient(color1, color2, 1 + (MAX_MINS // STEP))
alphas = [a for a in np.linspace(0.4, 0.8, 1 + (MAX_MINS // STEP))]

# audio = audio / max(audio)    # normalise
# audio = abs(audio)
prev_sample = [0]
for idx, i in enumerate(range(0, MAX_MINS, STEP)):
    sample = audio[sample_freq * 60 * i: sample_freq * 60 * (i + STEP)]
    sample = sample / max(sample)
    # sample = abs(sample)
    plt.plot(sample * idx, color=colours[idx], alpha=alphas[idx])
    prev_sample = sample

plt.ylabel("Amplitude (32-bit int PCM)")
plt.xlabel("Time (s)")
plt.show()

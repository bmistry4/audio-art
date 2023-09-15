import sys
import wave
import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read

from utils.plot_utils import get_color_gradient

SAVE = True
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
color1 = "#0F45D2"
color2 = "#bce1d0"

# 15 mins 38 secs == 983.0378333333333 secs
AUDIO_FILEPATH = sys.argv[1]

# len(audio) = no. data points/ samples
sample_freq, audio = read(AUDIO_FILEPATH)

# Check the data type of audio_data
data_type = audio.dtype
print(f"Data type of audio_data: {data_type}")

# Check the bit depth (number of bits per sample)
bit_depth = audio.dtype.itemsize * 8  # get number of bytes and mul by 8 to get no. of bits
print(f"Bit depth: {bit_depth} bits")


def time_domain_wave_exmaple():
    # https://dev.to/puritye/how-to-plot-an-audio-file-using-matplotlib-pbb
    obj = wave.open(AUDIO_FILEPATH, 'rb')
    print('Parameters:', obj.getparams())
    sample_freq = obj.getframerate()
    n_samples = obj.getnframes()
    signal_wave = obj.readframes(-1)
    duration = n_samples / sample_freq
    signal_array = np.frombuffer(signal_wave, dtype=np.int32)
    time = np.linspace(0, duration, num=n_samples)
    plt.figure(figsize=(15, 5))
    plt.plot(time, signal_array)
    plt.title('Audio Plot')
    plt.ylabel(' signal wave')
    plt.xlabel('time (s)')
    plt.xlim(0, duration)
    plt.show()


def plot_n_secs(data, n_sec, sample_fq, col, bit_depth):
    samples_to_plot = int(sample_fq * n_sec)
    t = np.linspace(0, n_sec, num=samples_to_plot)
    plt.plot(t[:samples_to_plot], data[:samples_to_plot], c=col)

    plt.title(f"Time Domain ({n_sec} secs)")
    plt.ylabel(f"Amplitude ({bit_depth}-bit int PCM)")
    plt.xlabel("Time (s)")
    plt.xlim(0, n_sec)


if __name__ == '__main__':
    # duration_secs = len(audio) / sample_freq
    # duration_mins = math.ceil(duration_secs / 60)
    # time = np.linspace(0, duration_secs, num=len(audio))
    # colours = get_color_gradient(color1, color2, duration_mins)
    #
    # # plot a minutes worth of data at a time. Each minute will have a different colour
    # samples_per_min = sample_freq * 60
    # for i in range(0, len(audio), samples_per_min):
    #     plt.plot(time[i:i + samples_per_min], audio[i:i + samples_per_min], c=colours[i // samples_per_min])
    #
    # plt.title("Time Domain")
    # plt.ylabel(f"Amplitude ({bit_depth}-bit int PCM)")
    # plt.xlabel("Time (s)")
    # plt.xlim(0, duration_secs)
    # if SAVE:
    #     plt.savefig('../images/time_domain_full.png')

    # plot_n_secs(audio, 0.001, sample_freq, color1, bit_depth)
    # if SAVE:
    #     plt.savefig('../images/time_domain_1e-3s.png')
    #
    plot_n_secs(audio, 10, sample_freq, color1, bit_depth)
    if SAVE:
        plt.savefig('../images/time_domain_10s.png')

    plt.show()
    print("completed")

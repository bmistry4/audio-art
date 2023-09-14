import numpy as np


def snip_audio(audio, time_range, sample_freq):
    # time range in minutes
    return audio[sample_freq ^ 60 * time_range[0]:sample_freq * 60 * (time_range[1] + 1)]


def convert_to_bins(audio, bins):
    # truncate audio to fill bins evenly
    num_allowed_dps = bins * (len(audio) // bins)
    print("Number of data points dropped: ", len(audio) - num_allowed_dps)
    audio = audio[:num_allowed_dps]

    # reshape audio to [bins, data points]
    audio = audio.reshape(bins, -1)
    print("Audio data matrix shape: ", audio.shape)
    return audio


def sparsify_audio(audio, max_samples_per_bin):
    # keep dropping every other column to sparsify data - it's crude, but it works
    while audio.shape[1] > max_samples_per_bin:
        audio = np.delete(audio, list(range(0, audio.shape[1], 2)), axis=1)
    print("Audio with every nth col deleted: ", audio.shape)
    return audio


def complex2polar(z: np.ndarray):
    # given array of complex numbers, convert each complex number (a + bi) to its polar coords (mag, phase)
    # equiv to sqrt(real^2 + im^2)
    mags = np.abs(z)
    # equiv to tan^-1(y/x) i.e., np.arctan(z[i].imag/ z[i].real)
    phases = np.angle(z)
    return mags, phases

def normalize_complex_coords(z):
    norms = np.linalg.norm(z, axis=-1, keepdims=True)
    return z / norms
import numpy as np


def snip_audio(audio, time_range, sample_freq):
    # time range in minutes
    return audio[sample_freq ^ 60 * time_range[0]:sample_freq * 60 * (time_range[1] + 1)]


def truncate_and_convert_to_bins(data, bins):
    """
    Split data to be in bins.
    Does not require data to already have perfect split. Will truncate any additional points.
    Assumes that data is 1D
    :param data: audio sample
    :param bins:
    :return:
    """
    if data.ndim != 1:
        raise Exception(f"Require 1D array for bin conversion. Data has {data.ndim} dims.")
    # truncate audio to fill bins evenly
    num_allowed_dps = bins * (data.size // bins)
    print("Number of data points dropped from reshape: ", data.size - num_allowed_dps)
    data = data[:num_allowed_dps]
    print("Data after dropping points: ", data.shape)

    # reshape audio to [bins, data points]
    data = data.reshape(bins, -1)
    print("Audio data matrix shape: ", data.shape)
    return data


def sparsify_audio(data, max_samples, method="drop"):
    """
    Assumes data is 2D [bins, dp] where bins=1
    :param data:
    :param max_samples:
    :param method:
    :return:
    """
    if data.shape[1] < max_samples:
        print("Data shape already within max samples. Nothing to sparsify.")
        return data

    if method == "drop":
        # keep dropping every other column to sparsify data - can overdrop so samples per bin is less than max_samples_per_bin
        while data.shape[1] > max_samples:
            data = np.delete(data, list(range(0, data.shape[1], 2)), axis=1)
    elif method == "random":
        output = np.zeros((data.shape[0], max_samples))
        for i in range(data.shape[0]):
            output[i, :] = np.random.choice(data[i, :], max_samples, replace=False)
        data = output
    # todo - could have donne sliding windows like in CNNs for more flexibility but that's overkill
    elif method == 'window-and-random':
        window_size = data.shape[1] // max_samples
        if window_size == 1:
            data = sparsify_audio(data, max_samples, method='random')
        else:
            num_windows = int(data.shape[1] / window_size)
            output = np.zeros((data.shape[0], num_windows))
            for b in range(data.shape[0]):
                means = np.empty(num_windows)
                for i in range(num_windows):
                    window_start = i * window_size
                    window_end = window_start + window_size
                    window_data = data[b, window_start:window_end]
                    mean = np.mean(window_data)
                    means[i] = mean
                output[b, :] = means
            data = output

        if data.shape[1] > max_samples:
            data = sparsify_audio(data, max_samples, method='random')
    else:
        raise KeyError(f"Sparsify method '{method}' does not exist!")
    return data


def apply_preprocessing(audio, samples_per_bin, num_bins, sparsify_method='random'):
    print("Initial total samples:", len(audio))
    total_samples = samples_per_bin * num_bins
    print("Total allowed samples: ", total_samples)

    # todo - mention in readme: sparsify 1st to avoid truncating end points
    audio = sparsify_audio(audio.reshape(1, -1), total_samples, method=sparsify_method)
    print("Sparsified audio: ", audio.shape)

    audio = truncate_and_convert_to_bins(audio.flatten(), num_bins)
    print("Total samples after preprocessing\n", audio.size)

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

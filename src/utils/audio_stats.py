########################################################################################################################
# PRINT BASIC AUDIO STATS - https://realpython.com/python-scipy-fft/
########################################################################################################################

"""
sample freq: 48000 Hz,
no. samples: 45025816 data points,
audio len: 938.0378333333333 secs,
no. channels: 1
"""
import sys
import wave

AUDIO_FILEPATH = sys.argv[1]

with wave.open(AUDIO_FILEPATH, 'rb') as wav_obj:
      sample_freq = wav_obj.getframerate()      # number of samples per second
      n_samples = wav_obj.getnframes()          # number of individual frames, or samples
      t_audio = n_samples / sample_freq         # audio length (secs)
      n_channels = wav_obj.getnchannels()       # no. channels e.g. if recorded in stereo = 2 channels (left and right)

      print(f"sample freq: {sample_freq} Hz,\n"
            f"no. samples: {n_samples} data points,\n"
            f"audio len: {t_audio} secs,\n"
            f"no. channels: {n_channels}"
            )

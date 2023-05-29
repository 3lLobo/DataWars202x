"""
The data hidden in the video can be found using spectroanlysis. 
During the CTF we ended up using webfft.net instead however similar tools 
like audacity would work. The Python script didnt provide an image of readable quality.

"A spectrogram is a visual representation of the spectrum of frequencies of a signal as it varies with time."
"""

import matplotlib.pyplot as plt
#from scipy.fft import fftshift
#from scipy.fftpack import fft
from scipy.io import wavfile
import scipy.signal

sample_rate, audio_time_series = wavfile.read("opdrachten\intel4\input.wav", )

# The data contains 1 row per sample
# So for 8.5 seconds, 375092 rows.
print(audio_time_series.shape[0]/sample_rate)

# Get the timeframe of the distortion.
time_series = audio_time_series[int(sample_rate*5.7):int(sample_rate*6.9), 0]

f, t, Sxx  = scipy.signal.spectrogram(time_series, sample_rate)

plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
# You can see the text but it is not/poorly legible.


# By default, matplotlib uses linear scaling but we want more contrast...
# Do this, we can use a log-based normalization.
plt.pcolormesh(t, f, Sxx, norm="log",)
plt.show()

# Now it is legible.
# 8285DDC90D4E
# Correct!

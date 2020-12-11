# read wav or flac file and calculate quantiles

import soundfile as sf   # install in this workspace via:  python -m pip install soundfile
import numpy as np               #   python -m pip install numpy
import matplotlib.pyplot as plt  #   python -m pip install matplotlib
from scipy.signal import welch   #   python -m pip install scipy

sndFilename = '/home/val/PycharmProjects/wavQuantiles/NATURE11_09_02_21_20_2701.flac'

dBcal = 70   #  'Calibration factor selected so quiet periods around 100 dB broad band
Nfft = 1024  # some power of two used for Fast Fourier Transform via Welch algorithm
sndf = sf.SoundFile(sndFilename)

blocksize = 4096
channelChoice = 0
psd_Aves = []
psd_Matrix = []
f_values = []
cnt = 0
while sndf.tell() < len(sndf) - blocksize:
    data = sndf.buffer_read(blocksize, dtype='int16')
    if sndf.channels == 2:
        if channelChoice == -1:
            ch0 = np.average(np.abs(np.frombuffer(data, dtype='int16')[0::2]))
            ch1 = np.average(np.abs(np.frombuffer(data, dtype='int16')[1::2]))
            if ch0 > ch1:
                channelChoice = 0
            else:
                channelChoice = 1
        npData = np.frombuffer(data, dtype='int16')[channelChoice::2]
    else:
        npData = np.frombuffer(data, dtype='int16')
    f_values, psd_values = welch(npData, fs=sndf.samplerate, nfft=Nfft, scaling='spectrum')
            # psd_values is power spectral density from welch algorithm
            # f_values are corresponding frequency

    if psd_Aves == []:
        psd_Aves = psd_values
        psd_Matrix = psd_values
    else:
        psd_Aves += psd_values
        psd_Matrix = np.append(psd_Matrix, psd_values, axis = 0)
    cnt += 1

dBaves = 10 * np.log10(psd_Aves/cnt)

print('sample rate is ', sndf.samplerate)
for i in range(0, Nfft//2, 10):
    print(f_values[i], dBaves[i])

plt.plot(f_values, dBaves)

plt.show()
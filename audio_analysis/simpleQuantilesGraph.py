# read wav or flac file and calculate quantiles

import soundfile as sf   # install in this workspace via:  python -m pip install soundfile
import numpy as np               #   python -m pip install numpy
import matplotlib.pyplot as plt  #   python -m pip install matplotlib

sndFilename = '/home/val/PycharmProjects/wavQuantiles/NATURE11_09_02_21_20_2701.flac'

dBcal = 70   #  'Calibration factor selected so quiet periods around 100 dB broad band

sndf = sf.SoundFile(sndFilename)

blocksize = 4096
channelChoice = 0
aveSqr = []
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

    ave = np.average(np.square(npData))
    aveSqr.append(ave)
print(aveSqr)
print(np.min(aveSqr), np.max(aveSqr))


dB = dBcal + 10*np.log10(aveSqr)
print('dB %_below_dB')
qs = []
percents = []
for i in range(100):
    fraction = float(i)/100.0
    q = np.quantile(dB, fraction)
    print('{:0.2f} {:0.0f}'.format(q, fraction*100))
    qs.append(q)
    percents.append(fraction*100)

plt.plot(qs, percents)
plt.show()


import numpy as np
import numpy
from scipy.signal import butter, lfilter, freqz
from scipy.fftpack import fft,ifft
from scipy.signal import hilbert
from scipy.signal import find_peaks
import scipy
from data_reader import get_bearing_signal
import matplotlib.pyplot as plt
from glob import glob

#from get_data import *
#from data_processing importfault_freqs = [236.4, 296.8, 280.4] *
fault_freqs = {"bpfo":236.4, "bpfi":296.8, "rdf":280.4}



def butter_bandpass(lowcut, highcut, sampling_freq, order=5):
	"""
	Band pass filter parameters:
	-lowcut: Low cutoff frequency
	-highcut: High cutoff frequency
	-fs: sampling frequency, Hz
	-order: order of fitler
	"""
	nyq = 0.5 * sampling_freq
	low = lowcut / nyq
	high = highcut / nyq
	b, a = butter(order, [low, high], btype='band')
	return b, a

def butter_bandpass_filter(data, lowcut, highcut, sampling_freq, order=5):
	"""
	Filter data along one-dimension with a bandpass filter:
	-data: data to be analysed
	-lowcut: Low cutoff frequency
	-highcut: High cutoff frequency
	-fs: sampling frequency, Hz
	-order: order of fitler
	"""

	b, a = butter_bandpass(lowcut, highcut, sampling_freq, order=order)
	y = lfilter(b, a, data)
	return y

## Low pass filter:
def butter_lowpass(cut, fs, order=5):
	"""
	Low pass filter parameters:
	-lowcut: Low cutoff frequency
	-fs: sampling frequency, Hz
	-order: order of fitler
	"""
	nyq = 0.5 * fs
	high = cut / nyq
	b, a = butter(order,  high, btype='low')
	return b, a

def butter_lowpass_filter(data, cut, fs, order=5):
	"""
	Filter data along one-dimension with a lowpass filter:
	-data: data to be analysed
	-lowcut: Low cutoff frequency
	-fs: sampling frequency, Hz
	-order: order of fitler
	"""
	b, a = butter_lowpass(cut, fs, order=order)
	y = lfilter(b, a, data)
	return y

## Envelop detection
def get_envelop(data):
	"""
	using Hilbert for envelop detection:
	data: data to be analysed
	"""
	hilbert_transform = hilbert(data)
	envelop = np.sqrt(data**2 + hilbert_transform**2)
	return envelop



def get_fft(signal,period,sampling_interval):
    signal_length = len(signal)
    sampling_freq = signal_length/period
    k = np.arange(signal_length)
    two_side_freq = k/period
    one_side_freq = two_side_freq[range(int(signal_length/2))]
    yf = fft(signal)
    freq = np.linspace(0.0, 1.0/(2.0*sampling_interval), signal_length//2)
    amplitude = 2.0/signal_length * np.abs(yf[:signal_length//2])*9.81
    amplitude[0] = 0
    return freq, amplitude


def get_envelop_spectrum(accelaration):
    lowcut = 2000
    highcut = 9990
    # sampling_freq = 9600
    # period = 2999.895996/1000
    # sampling_interval = 0.104166/1000
    sampling_freq = 20000
    period = 1
    sampling_interval = 1./20480
    y = butter_bandpass_filter(accelaration,lowcut,highcut,sampling_freq,order=5)
    envelop = get_envelop(y)
    low_pass = butter_lowpass_filter(envelop,2000,sampling_freq,order=5)
    freq, amplitude = get_fft(low_pass,period,sampling_interval)
    return freq, amplitude



def get_fault_frequency(signal,fault_freq):
	"""
	"""
	frequency,amplitude = get_envelop_spectrum(signal)
	found_frequency = list(filter(lambda f: round(f,0) == round(fault_freq,0) ,frequency))
	if len(found_frequency) == 1:
		idx = list(frequency).index(found_frequency[0])
		found_amplitude = amplitude[idx]
		return found_amplitude
	else:
		return None


if __name__ == '__main__':
    exp_nb = "2"
    meta_path = "metadata.yaml"
    files_path = f"../data/IMS/{exp_nb}/**"
    bearing_nb = 4
    fault_freq = fault_freqs["bpfo"]
    files = glob(files_path)
    files.sort()
    faults = []
    file_path = files[0]
    for file_path in files:
        y, fs = get_bearing_signal(file_path, meta_path, exp_nb, bearing_nb)
        fault = get_fault_frequency(y, fault_freq)

        faults.append(fault[0])
    #freq, amplitude = get_envelop_spectrum(y)
    plt.plot(faults)
    plt.show()


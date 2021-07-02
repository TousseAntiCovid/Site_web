
import os
import librosa
import librosa.display
import IPython.display as ipd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy import fftpack
from scipy import signal
import soundfile as sf
from os.path import basename


def plot_spectrogram(Y, sr, hop_length, y_axis="linear"):
    plt.figure(figsize=(25, 10))
    librosa.display.specshow(Y, sr=sr, hop_length=hop_length, x_axis="time", y_axis=y_axis)
    plt.colorbar(format="%+2.f")
    

def convert_to_fourier(cov_file):
    fileName, fileExtension = os.path.splitext(cov_file)
    scale, sr = librosa.load(cov_file)
    fourier = fftpack.fft(scale)
    power = np.abs(fourier) 
    frequences = fftpack.fftfreq(scale.size)
    fourier[ power < np.percentile(power,90) ] = 0
    filtered_signal = fftpack.ifft(fourier)
    FRAME_SIZE = 2048
    HOP_SIZE = 512
    S_scale = librosa.stft(np.abs(filtered_signal), n_fft=FRAME_SIZE, hop_length=HOP_SIZE)
    Y_scale = np.abs(S_scale) ** 2
    Y_log_scale = librosa.power_to_db(Y_scale)
    plot_spectrogram(Y_log_scale, sr, HOP_SIZE, y_axis="log")
    fileName1, fileExtension = os.path.splitext(cov_file)
    fileName1 = str(fileName1)
    
    for char in fileName1:
        if char == "/":
            fileName1 = fileName1.replace(char,'_')
            
    fileName1 = fileName1 + ".png"
    plt.savefig(str(fileName1))


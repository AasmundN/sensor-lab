from scipy.fft import fft, fftshift
import numpy as np

# Calculate effect spectrum for a give data set
def calc_spectrum(data, NFFT=4096):
    print("calc_spectrum is running")
    X = fft(data, NFFT)
    X_shifted = fftshift(X)

    Sx_dB = 20 * np.log10(np.abs(X_shifted) / np.max(np.abs(X)))

    print("calc_spectrum is done running")
    return Sx_dB


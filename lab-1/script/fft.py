import numpy as np
from scipy.fft import fft, fftshift

NFFT_choosen_too_low_error = "\nThe resolution of your FFT was choosen too low\nChoose a resolution higher than the lenght of the signal.\n"

NFFT_not_optimal_error = "\nThe resolution of your FFT is not two to the power of N. The FFT algorithm works best for when NFFT = 2^N."


# Calculate effect spectrum for a give data set
def calc_spectrum(data, NFFT):
    # If NFFT is less than the length of data, information is lost
    if NFFT < len(data):
        print(NFFT_choosen_too_low_error)
        print(
            f"The lenght of your signal was: {len(data)}. The closest power of two to your data lenght is: {round(2**(np.ceil(np.log2(len(data)))))}.\n"
        )
        exit(-1)

    if not np.log2(NFFT).is_integer():
        print(NFFT_not_optimal_error)
        print(
            f"The lenght of your signal was: {len(data)}. The closest power of two to your data lenght is: {round(2**(np.ceil(np.log2(len(data)))))}.\n"
        )
        exit(-1)

    X = fft(data, NFFT)

    Sx_dB = 20 * np.log10(abs(X) / max(abs(X)))

    Sx_dB_shifted = fftshift(Sx_dB)

    return Sx_dB_shifted

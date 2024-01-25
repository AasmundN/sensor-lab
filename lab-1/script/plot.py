import matplotlib.pyplot as plt

from scipy.fft import fftfreq, fftshift


def time_plot(data, time_max=1, sample_period=3.2e-5, label=""):
    pass


def spectrum_plot(data, sample_period=3.2e-5, label=""):
    print("spectrum_plot is running")
    NFFT = len(data)
    Fs = 1/sample_period
    df = Fs/NFFT
    f = fftfreq(NFFT, df)
    f_shifted = fftshift(f)

    print("spectrum_plot is done running")

    plt.plot(f_shifted, data)
    plt.grid()
    plt.show()



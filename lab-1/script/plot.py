import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fftfreq, fftshift

# adc resolution
resolution = 0.8e-3


def bode_plot(data_x, data_y, title="", show_plot=True):
    plt.plot(data_x, data_y)

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude [dB]")
    plt.title(title)

    plt.grid(linestyle=":")
    plt.tight_layout()
    plt.xscale("log")

    # allows modification of the plot outside of the function
    if not show_plot:
        return

    plt.show()


def time_plot(data, sample_period, title="", show_plot=True):
    # create scaled time axis
    t = np.arange(0, (len(data) - 0.5) * sample_period, sample_period)

    # convert data to voltage
    voltage = data * resolution

    # change time axis to ms
    t = t * 1e3

    plt.plot(t, voltage)

    plt.xlabel("Time [ms]")
    plt.ylabel("Voltage [V]")
    plt.title(title)

    plt.tight_layout()
    plt.grid()

    # allows modification of the plot outside of the function
    if not show_plot:
        return

    plt.show()


def spectrum_plot(data, sample_period, title="", show_plot=True):
    NFFT = len(data)
    Fs = 1 / sample_period
    df = Fs / NFFT

    f = np.arange(-Fs / 2, Fs / 2, df)

    plt.figure().set_figwidth(12)
    plt.plot(f, data, linewidth=0.8)

    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Relative effect [dB]")
    plt.title(title)

    plt.tight_layout()
    plt.grid()

    # allows modification of the plot outside of the function
    if not show_plot:
        return

    plt.show()

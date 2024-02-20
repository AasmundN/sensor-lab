import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fftfreq, fftshift, fft

# adc resolution
resolution = 0.8e-3


def sampling_example():
    Fs = 15
    F = 1

    N = 20
    NFFT = 20

    n = np.arange(0, N)

    x = np.sin(2 * np.pi * F * n / Fs)

    plt.plot(x, linewidth=3, marker=".", markersize=12)

    plt.xlabel("Målepunkt")
    plt.ylabel("Amplitude")

    plt.xticks([0, 5, 10, 15])

    plt.grid()
    plt.tight_layout()
    plt.show()

    X = fft(x, NFFT)
    X = fftshift(X)

    f = fftfreq(NFFT) * Fs
    f = fftshift(f)

    print(f)

    plt.plot(f, abs(X), linewidth=3)

    plt.xlabel("Frekvens [Hz]")
    plt.ylabel("Magnitude")

    plt.grid()
    plt.tight_layout()
    plt.show()


def bode_example():
    L = 100e-3
    C1 = 100e-6
    C2 = 0

    f = np.arange(5, 1000, 1e-1)
    w = 2 * np.pi * f

    H = 1 / (1 - w**2 * L * (C1 + C2))

    plt.plot(f, 10 * np.log10(abs(H)), linewidth=3)

    plt.xlabel("Frekvens [Hz]")
    plt.ylabel("Magnitude [dB]")

    plt.xscale("log")
    plt.tight_layout()
    plt.grid()
    plt.show()


def quantization_example():
    x = [-4, -2, 0, 2, 4]
    y = [-4, -2, 0, 2, 4]

    lines = plt.step(x, y, where="mid", linewidth=3)
    lines = plt.plot(x, y, linewidth=3, color="gray", alpha=0.2)

    axes = lines[0].axes
    xticks = list(axes.get_xticks())
    yticks = list(axes.get_yticks())

    plt.xticks(xticks, [])
    plt.yticks(yticks, [])

    # plt.xlim([-4.5, 4.5])
    # plt.ylim([-4.5, 4.5])

    plt.xlim([-4, 4.5])
    plt.ylim([-4, 4.5])

    axes.spines.right.set_visible(False)
    axes.spines.top.set_visible(False)

    plt.xlabel("Analog inngang")
    plt.ylabel("Kvantisert utgang")

    axes.set_aspect("equal", adjustable="box")

    plt.tight_layout()
    plt.show()


def bode_plot(data_x, data_y, title="", show_plot=True):
    plt.axhline(-3, linewidth=1, color="gray")
    plt.axvline(19.5655, linewidth=1, color="gray")
    plt.text(24, 0, "Knekkfrekvens: 19.5 Hz")

    plt.plot(data_x, data_y, linewidth=3)

    plt.xlabel("Frekvens [Hz]")
    plt.ylabel("Magnitude [dB]")
    plt.title(title)

    plt.grid(linestyle=":")
    plt.tight_layout()
    plt.xscale("log")

    # allows modification of the plot outside of the function
    if not show_plot:
        return

    plt.savefig("../img/filter.png")
    plt.show()


def time_plot(data, sample_period, title="", show_plot=True):
    # create scaled time axis
    t = np.arange(0, (len(data) - 0.5) * sample_period, sample_period)

    # convert data to voltage
    voltage = data * resolution

    # change time axis to ms
    t *= 1e3

    plt.plot(t, voltage, linewidth=3, marker=".", markersize=12)

    plt.xlabel("Tid [ms]")
    plt.ylabel("Spenning [V]")
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

    f /= 1000

    noise_max = round(np.max(data[60000:180000]) * 10) / 10
    print(noise_max)

    # plt.figure().set_figwidth(12)
    lines = plt.plot(f, data, linewidth=2, label=r"$S_x(k)$")

    ax = lines[0].axes
    ax.set_xticks(list(ax.get_xticks()) + [-2, 2])
    ax.set_yticks([0, -25, -50, -100, -125, -150, noise_max])

    # plt.xlim([-Fs / 2000, Fs / 2000])
    plt.xlim([0, Fs / 2000])

    plt.axhline(
        noise_max, color="orange", linestyle="--", linewidth=2, label="Støy maks"
    )

    plt.ylim([-160, 10])

    plt.xlabel("Frekvens [kHz]")
    plt.ylabel("Relativ effekt [dB]")
    plt.title(title)

    plt.legend()
    plt.tight_layout()
    plt.grid()

    # allows modification of the plot outside of the function
    if not show_plot:
        return

    plt.show()


if __name__ == "__main__":
    plt.rcParams["font.size"] = 16
    # sampling_example()
    # quantization_example()
    bode_example()

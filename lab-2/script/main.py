import sys
import os
from math import degrees
import numpy as np
import matplotlib.pyplot as plt

from raspi_import import raspi_import
from plot import time_plot, spectrum_plot, bode_plot
from fft import calc_spectrum
from scipy.signal import detrend

#
# To remove dc offset use scipy detrend
#

missing_file_path_error = (
    "\nMissing file path\n\nUsage example: python main.py foo.bin\n"
)


def correlation_test_plot():
    Fs = 50
    T = 1 / Fs
    samples = 100

    n = np.arange(0, samples / Fs, T)
    l = np.arange(-samples + 1, samples)

    sig_1 = np.sinc(2 * np.pi * n - np.pi)
    sig_2 = np.sinc(2 * np.pi * n - 1.2 * np.pi)

    correlation = np.correlate(sig_1, sig_2, "full")

    max_index = np.argmax(np.abs(correlation))

    fig, ax = plt.subplots(2)

    #
    # Time signals
    #
    ax[0].plot(sig_1, marker=".")
    ax[0].plot(sig_2, marker=".")
    ax[0].axvline(0, color="gray", alpha=0.5, linewidth=0.8)

    ax[0].set_title("Time signals")
    ax[0].set_xlabel("Sample number")
    ax[0].set_ylabel("Amplitude")

    #
    # Correlation
    #
    ax[1].plot(l, correlation, marker=".")
    ax[1].axvline(0, color="gray", alpha=0.5, linewidth=0.8)
    ax[1].axvline(l[max_index], color="gray", alpha=0.5, linewidth=0.8)

    ax[1].set_title("Correlation")
    ax[1].set_xlabel("Lag")
    ax[1].set_ylabel("Amplitude")

    fig.tight_layout()
    fig.set_figwidth(10)
    fig.set_figheight(6)

    plt.show()


def calc_angle(n12, n13, n23):
    numerator = np.sqrt(3) + n12 + n13
    denumenator = n12 - n13 - 2 * n23

    angle = np.arctan(numerator / denumenator)

    if denumenator < 0:
        angle += np.pi

    return angle


def estimate_angle(sample_period, data):
    sound_start = 10000
    sound_end = 15000

    #
    # Detrend and plot sound data
    #
    for i in range(2, 5):
        data[:, i] = detrend(data[:, i])
        # time_plot(
        #     data[sound_start:sound_end, i],
        #     sample_period,
        #     title=f"Sound signal {i - 1}",
        #     show_plot=False,
        # )

    sound = [
        data[sound_start:sound_end, 4],
        data[sound_start:sound_end, 2],
        data[sound_start:sound_end, 3],
    ]

    #
    # interpolate samples
    #

    interpolation_factor = 8

    x = np.arange(0, len(sound[0]) * sample_period, sample_period)
    x_vals = np.arange(
        0, len(sound[0]) * sample_period, sample_period / interpolation_factor
    )

    # _, ax = plt.subplots(2)

    # ax[0].plot(x[:50], sound[0][:50], marker=".")

    for i in range(3):
        sound[i] = np.interp(x_vals, x, sound[i])

    # ax[1].plot(x_vals[:100], sound[0][:100], marker=".")

    # plt.show()

    # sys.exit(1)

    #
    # find cross correlation and max lag
    #

    corr = [
        np.correlate(sound[1], sound[0], "full"),
        np.correlate(sound[2], sound[0], "full"),
        np.correlate(sound[2], sound[1], "full"),
    ]

    lags = {
        "n12": 0,
        "n13": 0,
        "n23": 0,
    }

    num_samples = len(sound[0])
    l = np.arange(-num_samples + 1, num_samples)

    for i in range(3):
        # index of max value
        max_index = np.argmax(np.abs(corr[i]))
        delay = l[max_index]
        lags[list(lags.keys())[i]] = delay

        plt.plot(l, corr[i])

        plt.title(f"Correlation \nLag: {delay}")
        plt.xlabel("Lag")
        plt.ylabel("Amplitude")

        # plt.show()

    #
    # estimate angle
    #

    angle = calc_angle(**lags)

    angle = 180 * angle / np.pi

    if angle > 180:
        angle -= 360

    return round(angle * 1000) / 1000


def main():
    # file path must be provided as argument
    if len(sys.argv) != 2:
        print(missing_file_path_error)
        exit(-1)

    path = sys.argv[1]

    if not os.path.isdir(path):
        sample_period, data = raspi_import(path)
        angle = estimate_angle(sample_period, data)
        print(angle)

        sys.exit(1)

    angles = [
        estimate_angle(*raspi_import(path + file))
        for file in os.listdir(path)
        if file != ".DS_Store"
    ]

    angles = sorted(angles, key=float)

    std = np.std([abs(el) for el in angles])

    print(angles, f"STD: {std}")


if __name__ == "__main__":
    main()

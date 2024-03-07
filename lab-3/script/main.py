import numpy as np
import matplotlib.pyplot as plt
from scipy.signal.windows import hann
from scipy.signal import detrend, filtfilt, butter
import os
import sys


def estimate_pulse(data, color, specter=True):
    if specter:
        data = data * hann(len(data))
    data = detrend(data)

    if not specter:
        plt.plot(data, color=color)

    NFFT = 2**20
    Fs = 40

    nyquist = Fs / 2
    low = 0.5 / nyquist
    high = 4 / nyquist

    b, a = butter(4, Wn=[low, high], btype="band")
    data = filtfilt(b, a, data)

    frequency = np.fft.fft(data, NFFT)
    frequency = np.fft.fftshift(frequency)

    df = Fs / NFFT
    f = np.arange(-Fs / 2, Fs / 2, df)

    middle = int(NFFT / 2)
    spectrum = 20 * np.log10(abs(frequency) / max(abs(frequency)))

    top = 5

    frequency = frequency[middle : int(middle + top / df)]
    spectrum = spectrum[middle : int(middle + top / df)]
    f = f[middle : int(middle + top / df)]

    pulse = 60 * f[np.argmax(spectrum)]

    # SNR = sum(frekvensbøtter med signal)/sum(frekvensbøtter med støy) (snitt kan også brukes)

    if specter:
        sig_start = np.argmax(spectrum) - 5000
        sig_stop = np.argmax(spectrum) + 5000

        snr = np.sum(spectrum[sig_start:sig_stop]) / (
            np.sum(spectrum[:sig_start]) + np.sum(spectrum[sig_stop:])
        )

        plt.axvline(f[sig_start])
        plt.axvline(f[sig_stop])

        print("SNR: ", snr)

    if specter:
        plt.plot(f, spectrum, color=color)

    return round(pulse * 100) / 100


def main():
    # file path must be provided as argument
    if len(sys.argv) != 2:
        exit(-1)

    path = sys.argv[1]

    start = 500
    end = -1

    colors = ["red", "green", "blue"]

    plt.rcParams["figure.figsize"] = (12, 5)

    if not os.path.isdir(path):
        data = np.genfromtxt(path, delimiter=" ")

        for i in range(3):
            pulse = estimate_pulse(data[start:end, i], colors[i], specter=False)

            print(colors[i], " ", pulse)

        plt.show()

        for i in range(3):
            pulse = estimate_pulse(data[start:end, i], colors[i], specter=True)

            print(colors[i], " ", pulse)

        plt.xlabel("Frekvens [Hz]")
        plt.ylabel("Relativ effekt [dB]")

        plt.show()

        sys.exit(1)

    for i in range(3):
        pulses = [
            estimate_pulse(
                np.genfromtxt(f"{path}{file}", delimiter=" ")[start:end, i], colors[i]
            )
            for file in os.listdir(path)
            if file != ".DS_Store"
        ]

        pulses = sorted(pulses, key=float)

        std = np.std([abs(el) for el in pulses])

        print(colors[i], " ", pulses, f"STD: {std}")


if __name__ == "__main__":
    main()

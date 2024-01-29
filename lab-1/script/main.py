import sys
from scipy.signal.windows import hann
import numpy as np

from raspi_import import raspi_import
from plot import time_plot, spectrum_plot, bode_plot
from fft import calc_spectrum

missing_file_path_error = (
    "\nMissing file path\n\nUsage example: python main.py foo.bin\n"
)

BIT_RESOLUTION = 4096
V_REF = 3.3
DC_OFFSET = 1


def main():
    # file path must be provided as argument
    if len(sys.argv) != 2:
        print(missing_file_path_error)
        exit(-1)

    file_path = sys.argv[1]

    #
    # import adc data and remove dc component
    #
    sample_period, data = raspi_import(file_path)
    dc_component = DC_OFFSET / V_REF * BIT_RESOLUTION
    data = data - dc_component

    #
    # import filter data
    #
    filter_data = np.genfromtxt(
        "/Users/aasmundnorsett/Documents/NTNU/Semester6/Sensor/sensor-lab/lab-1/data/filter.csv",
        delimiter=",",
    )

    bode_plot(filter_data[:, 0], filter_data[:, 1])

    #
    # example: plot slice of first data column
    #
    time_plot(data[2000:2100, 0], sample_period, show_plot=True)

    #
    # example: caluculate and plot power spectrum with and wihtout hann window
    #
    NFFT = 8192
    data_slice = data[2000:8000, 0]

    data_spec = calc_spectrum(data_slice, NFFT)
    spectrum_plot(data_spec, sample_period, show_plot=True)

    data_windowed = data_slice * hann(len(data_slice))

    data_spec = calc_spectrum(data_windowed, NFFT)
    spectrum_plot(data_spec, sample_period, show_plot=True)


if __name__ == "__main__":
    main()

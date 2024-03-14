from raspi_import import raspi_import
from plot import read_csv_with_header, bode_plot, spectrum_plot, time_plot
from fft import calc_spectrum

from scipy.signal import hann

missing_file_path_error = (
    "\nMissing file path\n\nUsage example: python main.py foo.bin\n"
)

BIT_RESOLUTION = 4096
V_REF = 3.3
DC_OFFSET = 1


def main():
    #
    # import adc data and remove dc component
    #
    sample_period, data = raspi_import(file_path)

    dc_component = DC_OFFSET / V_REF * BIT_RESOLUTION
    data = data - dc_component

    time_plot(
        data, sample_period, title="Time plot of data", save_plot=True, show_plot=True
    )

    #
    # example: caluculate and plot power spectrum with and wihtout hann window
    #
    lower_bounds = 0
    upper_bounds = -1
    data_slice = data[lower_bounds:upper_bounds]

    NFFT = 524288

    data_spec, _ = calc_spectrum(data_slice, NFFT)
    spectrum_plot(data_spec, sample_period, save_plot=False, show_plot=True)

    data_windowed = data_slice * hann(len(data_slice))

    data_spec, _ = calc_spectrum(data_windowed, NFFT)
    spectrum_plot(data_spec, sample_period, save_plot=False, show_plot=True)


if __name__ == "__main__":
    main()

import sys

from raspi_import import raspi_import
from plot import time_plot, spectrum_plot
from fft import calc_spectrum

missing_file_path_error = (
    "\nMissing file path\n\nUsage example: python main.py foo.bin\n"
)


def main():
    # file path must be provided as argument
    if len(sys.argv) != 2:
        print(missing_file_path_error)
        exit(-1)

    file_path = sys.argv[1] or exit("Missing file path")

    # get sample data
    sample_period, data = raspi_import(file_path)

    spectrum = calc_spectrum(data)
    spectrum_plot(spectrum, sample_period)


if __name__ == "__main__":
    main()

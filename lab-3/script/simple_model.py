import numpy as np


def calc_mu(bvf, oxy):
    muabo = np.genfromtxt(
        "/Users/aasmundnorsett/Documents/NTNU/Semester6/Sensor/sensor-lab/lab-3/data/muabo.txt",
        delimiter=",",
    )
    muabd = np.genfromtxt(
        "/Users/aasmundnorsett/Documents/NTNU/Semester6/Sensor/sensor-lab/lab-3/data/muabd.txt",
        delimiter=",",
    )

    red_wavelength = 600  # Replace with wavelength in nanometres
    green_wavelength = 515  # Replace with wavelength in nanometres
    blue_wavelength = 460  # Replace with wavelength in nanometres

    wavelength = np.array([red_wavelength, green_wavelength, blue_wavelength])

    def mua_blood_oxy(x):
        return np.interp(x, muabo[:, 0], muabo[:, 1])

    def mua_blood_deoxy(x):
        return np.interp(x, muabd[:, 0], muabd[:, 1])

    # Absorption coefficient ($\mu_a$ in lab text)
    # Units: 1/m
    mua_other = 25  # Background absorption due to collagen, et cetera
    mua_blood = mua_blood_oxy(wavelength) * oxy + mua_blood_deoxy(  # Absorption due to
        wavelength
    ) * (
        1 - oxy
    )  # pure blood
    mua = mua_blood * bvf + mua_other

    # reduced scattering coefficient ($\mu_s^\prime$ in lab text)
    # the numerical constants are thanks to N. Bashkatov, E. A. Genina and
    # V. V. Tuchin. Optical properties of skin, subcutaneous and muscle
    # tissues: A review. In: J. Innov. Opt. Health Sci., 4(1):9-38, 2011.
    # Units: 1/m
    musr = 100 * (17.6 * (wavelength / 500) ** -4 + 18.78 * (wavelength / 500) ** -0.22)

    return (mua, musr)

    # mua and musr are now available as shape (3,) arrays
    # Red, green and blue correspond to indexes 0, 1 and 2, respectively


mua, musr = calc_mu(bvf=0.01, oxy=0.8)

delta = lambda mua, musr: 1 / np.sqrt(3 * mua * (mua + musr))

print("\nValues are given as RGB, in that order")

#
# 11.1a
#
deltatissue = delta(mua, musr)
print("Penetrationdepth: ", deltatissue)


#
# 11.1b
# Vi har probet hele fingeren, fordi dette er lys som er målt på andre siden
#
fingerwidth = 0.015
print("Transmitance [%]: ", 100 * np.exp(-fingerwidth / delta(mua, musr)))

#
# 11.1c
# Dette er like dypt som penetrasjonsdybden
#
print("Probedepth: ", deltatissue)

#
# 11.1d
#

# for blood vein
mua, musr = calc_mu(bvf=1, oxy=0.8)
deltavein = delta(mua, musr)

veinwidth = 300e-6
veintransmitance = np.exp(-veinwidth / deltavein)

tissuewidth = 300e-6
tissuetransmitance = np.exp(-tissuewidth / deltatissue)

K = abs(veintransmitance - tissuetransmitance) / tissuetransmitance
print("Contrast: ", K)

#
# Blue light would give the highest changes in the meassured light,
# making it easier to see variations due to changes in blood volume,
# giving a high pulse amplitude.
#

#
# 12.1
#
# We can devide the maximum pulse amplitude by the std of the noise.
#
# We can estimate the SNR in the frequency domain by picking out a frequency range
# of interest. For example 0 to 3-4 Hz for the pulse case. Then we can avarage the values
# in this bin and in the rest of the frequency domain and find the relationship between these two.
# This is assuming that the the rest of the frequencies only contain noise.

print("")

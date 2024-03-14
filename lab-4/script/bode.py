import csv  # reads .csv files
import matplotlib.pyplot as plt  # plots lists


#
# Reads csv values with header row from file in filepath,
# and returns the header and datapoints in two seperate lists
#
def readFromCsvWithHeader(filepath):
    header = []
    content = []

    with open(filepath) as csvfile:
        csvreader = csv.reader(csvfile)

        header = next(csvreader)

        for row in csvreader:
            #
            # Creates a list of the values on each row converted to floats
            #
            values = [float(value) for value in row]
            content.append(values)

        return header, content


#
# Plots the content of each list provided in the data list as a seperate plot,
# optional title argument gives each plot the title corresponding to same index as the data
#
def bodePlot(data_lst, titles=[]):
    for i in range(len(data_lst)):
        frequency = [row[0] for row in data_lst[i]]
        ch1 = [row[1] for row in data_lst[i]]
        ch2 = [row[2] for row in data_lst[i]]

        plt.figure(i + 1)

        # plt.plot(frequency, ch1, 'y', linewidth=3, marker=".", markersize=12)
        plt.plot(frequency, ch2, "b", linewidth=3, markersize=12)

        plt.xlabel("Frequency [Hz]")
        plt.ylabel("Magnitude [dB]")

        plt.xscale("log")
        plt.grid(True)
        plt.tight_layout()

        if len(titles) > 0:
            if i < len(titles):
                plt.title(titles[i])
                plt.savefig(
                    str("lab-4/img/" + titles[i]) + "-figure-" + str(i) + ".png",
                    dpi=300,
                    bbox_inches="tight",
                )
            else:
                plt.title("")
                plt.savefig("figure-" + str(i) + ".png", dpi=300, bbox_inches="tight")

    # plt.show()


if __name__ == "__main__":
    header_A, data_A = readFromCsvWithHeader("lab-4/data/bode-plot-filter-A.csv")
    header_B, data_B = readFromCsvWithHeader("lab-4/data/bode-plot-filter-B.csv")
    bodePlot([data_A, data_B], ["Bodeplot-A", "Bodeplot-B"])

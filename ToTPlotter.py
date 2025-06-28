from timepix4.tot import *


def main():
    # filepath = "Data/Filtered Calibration Data/N116-250408-123554-Filtered.csv"
    filepath = "Data/Filtered Calibration Data/N116-Charge-Data.csv"
    # filepath = "Data/Filtered Calibration Data/N116-filtered.csv"
    # filepath = "scaled_raw_data1.csv"
    # ToTPlotter(filepath=filepath, COL=228, ROW=230)
    FourToTPlotter(filepath=filepath)


if __name__ == "__main__":
    main()

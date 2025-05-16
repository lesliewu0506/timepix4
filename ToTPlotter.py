from timepix4.tot import ToTPlotter


def main():
    filepath = "Data/Filtered Calibration Data/N116-250408-123554-Filtered.csv"
    filepath = "N116-Charge-Data.csv"
    ToTPlotter(filepath=filepath, COL=238, ROW=240)


if __name__ == "__main__":
    main()

from timepix4.tot import ToTPlotter


def main():
    filepath = "Data/Filtered Calibration Data/N116-250408-123554-Filtered.csv"
    ToTPlotter(filepath=filepath, COL=229, ROW=230)


if __name__ == "__main__":
    main()

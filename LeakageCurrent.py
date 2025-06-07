from timepix4.leakage_current import PlotIV


def main():
    # PlotIV("Data/Voltage Scans/N116_voltage_scan.txt")
    PlotIV("Data/Voltage Scans/N116_IV.txt", MaxCurrent=2)

if __name__ == "__main__":
    main()

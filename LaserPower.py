from timepix4.laser_power import PowerVoltagePlot, CreateLookupTable, PlotRelativePower


def main():
    filepath = "Data/Laser Power/Power.csv"
    # PowerVoltagePlot(filepath)
    # filepath = "Data/Laser Power/laser_power_933nm.csv"
    CreateLookupTable(filepath)
    # PlotRelativePower("lookup_table.csv")
if __name__ == "__main__":
    main()

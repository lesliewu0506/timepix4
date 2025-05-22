from timepix4.laser_power import *


def main():
    filepath = "Data/Laser Power/Power.csv"
    # PowerVoltagePlot(filepath)
    # filepath = "Data/Laser Power/laser_power_933nm.csv"
    # CreateLookupTable(filepath, 3.750)
    # PlotRelativePower("lookup_table(230, 228).csv")
    PlotLaserStability("Data/Laser Power/Laser Stability/Laser_over_time_6ke.csv")
    # PlotClosestVoltage("Data/Laser Measurements/Laser Measurements 1/1Results(230, 228).csv", 158.09)

if __name__ == "__main__":
    main()

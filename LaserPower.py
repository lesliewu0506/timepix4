from timepix4.laser_power import *


def main():
    filepath = "Data/Laser Power/Power.csv"
    DirectRelativePower(filepath, 3.725)
    # CreateLookupTable(filepath, 3.725)
    # PlotRelativePower("lookup_table(230, 228).csv")
    # PlotLaserStability("Data/Laser Power/Laser Stability/Laser_over_time_6ke.csv")
    # PlotClosestVoltage("Data/Laser Measurements/High/Laser Measurements 1 (228, 230)/1Results(230, 228).csv", 158)

if __name__ == "__main__":
    main()

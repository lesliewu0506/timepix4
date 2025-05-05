from timepix4.manual_calibration import PlotManualCalibratedCharge


def main():
    filepath = "Data/Filtered Calibration Data/N116-250403-150114-Charge-Data.csv"
    PlotManualCalibratedCharge(filepath)


if __name__ == "__main__":
    main()

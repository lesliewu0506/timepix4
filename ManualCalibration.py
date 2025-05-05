from timepix4.manual_calibration import (
    PlotManualCalibratedCharge,
    GetCalibrationFactors,
)


def main():
    filepath = "Data/Filtered Calibration Data/N116-250403-150114-Charge-Data.csv"
    # PlotManualCalibratedCharge(filepath)
    filepath2 = "Data/Filtered Calibration Data/N116-250403-150114-Charge-Data.csv"
    GetCalibrationFactors(filepath2)


if __name__ == "__main__":
    main()

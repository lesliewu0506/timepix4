from timepix4.testpulseanalysis import *


def main():
    # ScalingFactors("Data/Filtered Calibration Data/N116-Charge-Data.csv")
    # RefactoredDistribution(
    #     "Data/Filtered Calibration Data/N116-Charge-Data.csv",
    #     # "Data/Filtered Calibration Data/N116-250403-150114-Charge-Data.csv",
    # )
    ScalingDistribution("scaling_factors1.csv")

if __name__ == "__main__":
    main()

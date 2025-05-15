from timepix4.laser_measurement import *


def Process():
    FolderPath = "Data/Laser Measurements/Laser Measurements 4 V3"
    processor = Processor(FolderPath, ROW=240, COL=238, COL_Next=1, ROW_Next=-1)
    processor.ProcessFolder()


def Plotter():

    folders = [
        "Data/Laser Measurements/Laser Measurements 1/1Results(230, 228).csv",
        # "Data/Laser Measurements/Laser Measurements 2/2Results(229, 228).csv",
        "Data/Laser Measurements/Laser Measurements 2/2Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 4/4Results(230, 228).csv",
        # "Data/Laser Measurements/Laser Measurements 4/4Results(229, 228).csv",
        # "Data/Laser Measurements/Laser Measurements 4/4Results(230, 229).csv",
        # "Data/Laser Measurements/Laser Measurements 4/4Results(229, 229).csv",
    ]
    # folders = [
    #     "Data/Laser Measurements/Laser Measurements 1/1Results(230, 228).csv",
    #     "Data/Laser Measurements/Laser Measurements 2/2AllPixels_SumResults.csv",
    #     "Data/Laser Measurements/Laser Measurements 4/4AllPixels_SumResults.csv",
    # ]
    # ToTChargePlotter(folders)
    # LaserPlotterMultiple(
    LaserPlotter(
        # "Data/Laser Measurements/Laser Measurements 1 V3/1Results(240, 238).csv",
        # "Data/Laser Measurements/Laser Measurements 2 V3/2Results(240, 238).csv",
        # "Data/Laser Measurements/Laser Measurements 4 V3/4Results(240, 238).csv",
        "Data/Laser Measurements/Laser Measurements 1/1Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 2/2Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 4/4Results(230, 228).csv",
        value="clCharge Calibrated",
    )
    # CompareMethodsPlotter(
    #     "Data/Laser Measurements/Laser Measurements 1/1Results(230, 228).csv"
    # )


def main():
    # Process()
    Plotter()


if __name__ == "__main__":
    main()

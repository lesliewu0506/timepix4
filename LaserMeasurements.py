from timepix4.laser_measurement import *


def main():
    # FolderPath = "Data/Laser Measurements/Laser Measurements 2"
    # processor = Processor(FolderPath, COL_Next=0, ROW_Next=-1)
    # processor.ProcessFolder()

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
    LaserPlotter(
        "Data/Laser Measurements/Laser Measurements 1/1Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 2/2Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 4/4Results(230, 228).csv",
        value="clCharge",
    )
    # CompareMethodsPlotter(
    #     "Data/Laser Measurements/Laser Measurements 1/1Results(230, 228).csv"
    # )


if __name__ == "__main__":
    main()

from timepix4.laser_measurement import Processor, ToTChargePlotter


def main():
    # FolderPath = "Data/Laser Measurements/Laser Measurements 4"
    # processor = Processor(FolderPath, COL_Next=1, ROW_Next=-1)
    # processor.ProcessFolder()
    # folders = [
    #     "Data/Laser Measurements/Laser Measurements 1 V2/1Results(230, 228).csv",
    #     "Data/Laser Measurements/Laser Measurements 2 V2/2Results(229, 228).csv",
    #     "Data/Laser Measurements/Laser Measurements 2 V2/2Results(230, 228).csv",
    # ]
    folders = [
        "Data/Laser Measurements/Laser Measurements 1 V2/1Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 4 V2/4Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 4 V2/4Results(229, 228).csv",
        "Data/Laser Measurements/Laser Measurements 4 V2/4Results(230, 229).csv",
        "Data/Laser Measurements/Laser Measurements 4 V2/4Results(229, 229).csv",
    ]
    folders = [
        "Data/Laser Measurements/Laser Measurements 1 V2/1Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 2 V2/2Results(229, 228).csv",
        "Data/Laser Measurements/Laser Measurements 2 V2/2Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 4/4Results(230, 228).csv",
        "Data/Laser Measurements/Laser Measurements 4/4Results(229, 228).csv",
        "Data/Laser Measurements/Laser Measurements 4/4Results(230, 229).csv",
        "Data/Laser Measurements/Laser Measurements 4/4Results(229, 229).csv",
    ]
    # ToTChargePlotter("Data/Laser Measurements/Laser Measurements 1 V2/1Results(230, 228).csv")
    ToTChargePlotter(folders)


if __name__ == "__main__":
    main()

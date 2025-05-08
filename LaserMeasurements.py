from timepix4.laser_measurement import Processor, ToTChargePlotter


def main():
    FolderPath = "Data/Laser Measurements/Laser Measurements 1 V2"
    processor = Processor(FolderPath)
    processor.ProcessFolder()
    ToTChargePlotter("Data/Laser Measurements/Laser Measurements 1 V2/Results.csv")


if __name__ == "__main__":
    main()

from timepix4.laser_measurement import Processor, ToTChargePlotter

def main():
    FolderPath = "Data/Laser Measurements/Laser Measurements 4"
    processor = Processor(FolderPath)
    processor.ProcessFolder()
    # ToTChargePlotter("Data/Laser Measurements/Results.csv")
if __name__ == "__main__":
    main()
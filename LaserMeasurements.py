from timepix4.laser_measurement import *


def Process():
#     processall()

    FolderPath = (
        f"Data/Laser Measurements/Laser Measurements 1 (238, 240)"
    )
    processor = Processor(
        FolderPath,
        ROW=240,
        COL=238,
        COL_Next=1,
        ROW_Next=-1,
    )
    processor.ProcessFolder()


def processall():
    for col in [228, 238]:
        for row in [230, 240]:
            for x in ["1", "2", "4"]:
                cnext = 0
                rnext = 0
                if x == "2":
                    cnext = 1
                    rnext = 0
                elif x == "4":
                    cnext = 1
                    rnext = -1
                FolderPath = (
                    f"Data/Laser Measurements/Low/Laser Measurements {x} ({col}, {row})"
                )
                processor = Processor(
                    FolderPath,
                    ROW=row,
                    COL=col,
                    COL_Next=cnext,
                    ROW_Next=rnext,
                )
                processor.ProcessFolder()
                print(f"Processed Laser Measurements {x} ({col}, {row})")


def Plotter():
    folder_228_230 = [
        "Data/Laser Measurements/x/Laser Measurements 1 (228, 230)/1Results(230, 228).csv",
        "Data/Laser Measurements/x/Laser Measurements 2 (228, 230)/2Results(230, 228).csv",
        "Data/Laser Measurements/x/Laser Measurements 4 (228, 230)/4Results(230, 228).csv",
    ]
    folder_228_240 = [
        "Data/Laser Measurements/x/Laser Measurements 1 (228, 240)/1Results(240, 228).csv",
        "Data/Laser Measurements/x/Laser Measurements 2 (228, 240)/2Results(240, 228).csv",
        "Data/Laser Measurements/x/Laser Measurements 4 (228, 240)/4Results(240, 228).csv",
    ]
    folder_238_230 = [
        "Data/Laser Measurements/x/Laser Measurements 1 (238, 230)/1Results(230, 238).csv",
        "Data/Laser Measurements/x/Laser Measurements 2 (238, 230)/2Results(230, 238).csv",
        "Data/Laser Measurements/x/Laser Measurements 4 (238, 230)/4Results(230, 238).csv",
    ]
    folder_238_240 = [
        "Data/Laser Measurements/x/Laser Measurements 1 (238, 240)/1Results(240, 238).csv",
        "Data/Laser Measurements/x/Laser Measurements 2 (238, 240)/2Results(240, 238).csv",
        "Data/Laser Measurements/x/Laser Measurements 4 (238, 240)/4Results(240, 238).csv",
    ]
    LaserPlotter(
        [
            folder_228_230,
            folder_228_240,
            folder_238_230,
            folder_238_240
        ],
        value="clCharge Calibrated",
    )


def main():
    # Process()
    Plotter()


if __name__ == "__main__":
    main()

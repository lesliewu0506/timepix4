from timepix4.converters import ConvertTestPulseData, ConvertClusterData


def convert_test_pulse_data() -> None:
    RootFilePath = "Data/Test Pulse Data/N116-250417-093801.root"
    # ChargeFilePath = "Data/Test Pulse Data/Charge Calibrations/N116_charge.txt"
    OutputPathData = "Data/Test Pulse Data"
    OutputPathResults = "Data/Test Pulse Data"
    # ConvertTestPulseData(
    #     RootFilePath, ChargeFilePath, OutputPathData, OutputPathResults
    # )
    ChargeFilePaths = [
        "Data/Test Pulse Data/Charge Calibrations/N10_charge.txt",
        "Data/Test Pulse Data/Charge Calibrations/N116_charge.txt",
        "Data/Test Pulse Data/Charge Calibrations/N112_charge.txt",
        "Data/Test Pulse Data/Charge Calibrations/N113_charge.txt",
    ]
    for filepath in ChargeFilePaths:
        ConvertTestPulseData(
            charge_file_path=filepath,
            output_path_results=OutputPathResults,
        )

def convert_cluster_data() -> None:
    RootFilePath = "Data/Am-241 Runs/N116-250408-105332.root"
    ConvertClusterData(RootFilePath)

def main():
    # convert_test_pulse_data()
    convert_cluster_data()


if __name__ == "__main__":
    main()

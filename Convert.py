from timepix4.converters import ConvertTestPulseData


def convert_test_pulse_data() -> None:
    RootFilePath = "Data/Test Pulse Data/N116-250417-093801.root"
    ChargeFilePath = "Data/Test Pulse Data/Charge Calibrations/N116_charge.txt"
    OutputPathData = "."
    OutputPathResults = "."
    ConvertTestPulseData(
        RootFilePath, ChargeFilePath, OutputPathData, OutputPathResults
    )


def main():
    convert_test_pulse_data()

if __name__ == "__main__":
    main()

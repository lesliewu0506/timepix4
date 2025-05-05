from timepix4.test_pulse_analysis import ParameterComparison


def parameter_comparison() -> None:
    filepath1 = "N116-TestPulseResults.csv"
    filepath2 = "N10-TestPulseResults.csv"
    ParameterComparison(filepath1, filepath2)


def main():
    parameter_comparison()


if __name__ == "__main__":
    main()

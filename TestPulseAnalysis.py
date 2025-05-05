from timepix4.test_pulse_analysis import (
    ParameterComparison,
    HeatmapFitParam,
    STDHistogramComparison,
)


def parameter_comparison() -> None:
    filepath1 = "N116-TestPulseResults.csv"
    filepath2 = "N10-TestPulseResults.csv"
    ParameterComparison(filepath1, filepath2)


def heatmap_fit_param() -> None:
    filepaths = [
        "N116-TestPulseResults.csv",
        "N10-TestPulseResults.csv",
        "N112-TestPulseResults.csv",
        "N113-TestPulseResults.csv",
    ]
    HeatmapFitParam(filepaths, parameter="p1")


def std_histogram_comparison() -> None:
    filepaths = [
        "Data/Test Pulse Data/N116-TestPulseData.csv",
        "Data/Test Pulse Data/N10-TestPulseData.csv",
        "Data/Test Pulse Data/N112-TestPulseData.csv",
        "Data/Test Pulse Data/N113-TestPulseData.csv",
    ]
    STDHistogramComparison(filepaths)


def main():
    # parameter_comparison()
    # heatmap_fit_param()
    std_histogram_comparison()


if __name__ == "__main__":
    main()

from timepix4.heatmap import PlotAvgToTHeatmap, PlotAvgToTAndFitHeatmaps


def main():
    filepath = "Data/Filtered Calibration Data/N116-250403-150114-Charge-Data.csv"
    # PlotAvgToTHeatmap(filepath)
    filefit = "Data/Test Pulse Data/N116-TestPulseResults.csv"
    PlotAvgToTAndFitHeatmaps(filepath, filefit)

if __name__ == "__main__":
    main()

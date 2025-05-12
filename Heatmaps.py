from timepix4.heatmap import PlotAvgToTHeatmap, PlotAvgToTAndFitHeatmaps, VisualizeToT


def main():
    # filepath = "Data/Filtered Calibration Data/N116-250403-150114-Charge-Data.csv"
    # # PlotAvgToTHeatmap(filepath)
    # filefit = "Data/Test Pulse Data/N116-TestPulseResults.csv"
    # PlotAvgToTAndFitHeatmaps(filepath, filefit)
    VisualizeToT("Data/Laser Measurements/Laser Measurements 4/3_350.root")

if __name__ == "__main__":
    main()
